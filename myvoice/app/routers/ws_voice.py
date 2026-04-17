"""
WebSocket Voice Router - /v1/kid/voice/{session_id}

Handles real-time voice communication between the frontend and AI.
Supports three modes based on VOICE_MODE config:
  - "realtime": OpenAI Realtime API (movice pattern - single connection)
  - "azure": Azure OpenAI Realtime API
  - "http": Legacy Whisper + GPT-4 + TTS pipeline (3 separate calls)

On connect, loads child profile + curriculum/activity context from DB
to enrich the VoiceSession for the 3-character prompt system.
"""
import logging
from datetime import date

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError
from sqlalchemy import select

from app.config import get_settings
from app.database import async_session_maker
from app.models.family import Child
from app.models.session import Session, SessionActivity
from app.models.curriculum import CurriculumUnit, Activity
from app.services.voice_proxy import (
    VoiceSession,
    # Realtime mode (movice pattern)
    handle_realtime_text,
    handle_realtime_audio,
    # Azure mode
    handle_azure_session,
    handle_azure_audio,
    # HTTP fallback mode
    handle_http_audio,
    handle_http_text,
    send_msg,
)
from app.services.prompt_builder import _get_mission_theme
from app.services.signal_interpreter import interpret_signal

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter()

# Max audio payload: 5MB base64 ~ 3.75MB raw audio ~ ~78s at 24kHz 16-bit mono
MAX_AUDIO_BASE64_LEN = 5 * 1024 * 1024


def _verify_child_token(token: str) -> str | None:
    """Verify child JWT token and return child_id."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload.get("sub") or payload.get("child_id")
    except JWTError:
        return None


async def _enrich_session(session: VoiceSession) -> None:
    """
    Load child profile + curriculum/activity context from DB.
    Populates VoiceSession fields used by the prompt builder.
    """
    try:
        async with async_session_maker() as db:
            # 1. Load child profile
            child = await db.get(Child, session.child_id)
            if child:
                session.child_name = child.name or ""
                session.child_level = child.level or 1
                session.child_language = child.primary_language or "ko"
                # Calculate age from birth_date
                if child.birth_date:
                    today = date.today()
                    bd = child.birth_date
                    if hasattr(bd, 'date'):
                        bd = bd.date()
                    session.child_age = today.year - bd.year - (
                        (today.month, today.day) < (bd.month, bd.day)
                    )
                logger.info(
                    f"Child loaded: {session.child_name}, age={session.child_age}, "
                    f"level={session.child_level}"
                )

            # 2. Load session + curriculum context (skip for free_talk)
            if session.session_id == "free_talk":
                session.session_type = "free_talk"
                return

            db_session = await db.get(Session, session.session_id)
            if not db_session:
                session.session_type = "free_talk"
                return

            session.session_type = db_session.session_type or "curriculum"

            # 3. Load curriculum unit
            if db_session.curriculum_unit_id:
                stmt = select(CurriculumUnit).where(
                    CurriculumUnit.curriculum_unit_id == db_session.curriculum_unit_id
                )
                result = await db.execute(stmt)
                unit = result.scalar_one_or_none()
                if unit:
                    session.unit_title = unit.title or ""
                    session.unit_description = unit.description or ""
                    session.unit_week = unit.week or 0
                    session.difficulty_level = unit.difficulty_level or 1
                    session.korean_ratio = unit.korean_ratio if unit.korean_ratio is not None else 50
                    session.target_skills = unit.target_skills or []
                    session.story_theme = unit.story_theme or "earth_crew"
                    logger.info(
                        f"Curriculum loaded: W{session.unit_week} '{session.unit_title}' "
                        f"difficulty={session.difficulty_level}"
                    )

            # 4. Load current activity (first non-completed activity in session)
            stmt = (
                select(SessionActivity)
                .where(SessionActivity.session_id == session.session_id)
                .order_by(SessionActivity.order_index)
            )
            result = await db.execute(stmt)
            session_activities = result.scalars().all()

            current_activity_id = None
            for sa in session_activities:
                if sa.status != "completed":
                    current_activity_id = sa.activity_id
                    break
            # Fallback to first activity
            if not current_activity_id and session_activities:
                current_activity_id = session_activities[0].activity_id

            if current_activity_id:
                stmt = select(Activity).where(
                    Activity.activity_id == current_activity_id
                )
                result = await db.execute(stmt)
                activity = result.scalar_one_or_none()
                if activity:
                    session.activity_name = activity.name or ""
                    session.activity_type = activity.activity_type or ""
                    session.instructions_for_ai = activity.instructions_for_ai or ""
                    session.story_content = activity.story_content or ""
                    session.key_expression = activity.key_expression or ""
                    session.intro_narrator_script = activity.intro_narrator_script or ""
                    session.outro_narrator_script = activity.outro_narrator_script or ""
                    logger.info(
                        f"Activity loaded: '{session.activity_name}' "
                        f"type={session.activity_type}"
                    )

    except Exception as e:
        logger.error(f"Failed to enrich session context: {e}", exc_info=True)
        # Non-fatal — session continues with defaults (free_talk behavior)


async def _send_adventure_opening(session: VoiceSession, websocket: WebSocket):
    """
    Auto-trigger the opening turn for curriculum sessions.

    Flow:
    1. If intro_narrator_script exists, play it as narrator TTS (immersive opening).
    2. Then trigger AI to generate the first interactive turn (Luna + Popo).
    """
    name = session.child_name or "캡틴"
    activity = session.activity_name or "모험"
    story = session.story_content or ""

    logger.info(f"Adventure opening trigger for session {session.session_id}")

    # Narrator intro is already played by the frontend (Phase 1 in AdventurePlay).
    # Here we only trigger the AI to generate the first interactive turn (Luna + Popo).
    opening_prompt = (
        f"[SYSTEM_OPENING] 오프닝 나레이션이 끝났습니다. 이제 캐릭터들이 연기를 시작합니다.\n"
        f"다음 순서로 첫 대화를 생성하세요:\n"
        f"1. 루나: 상황에 맞는 영어 대사로 연기를 시작하세요 (호기심/놀라움/서투른 영어).\n"
        f"2. 포포: {name} 캡틴에게 루나를 도와달라고 부드럽게 유도하세요.\n"
        f"나레이션은 이미 재생되었으므로 [나레이션] 태그는 사용하지 마세요.\n"
    )
    if story:
        opening_prompt += f"\n스토리 배경: {story}\n"
    if activity:
        opening_prompt += f"활동: {activity}\n"

    mode = settings.voice_mode
    if mode == "realtime":
        await handle_realtime_text(session, opening_prompt)
    elif mode == "azure":
        content = [{"type": "input_text", "text": opening_prompt}]
        session.add_message("user", opening_prompt)
        await send_msg(websocket, {
            "type": "transcript",
            "role": "user",
            "text": opening_prompt,
        })
        await handle_azure_session(session, content)
    else:
        await handle_http_text(session, opening_prompt)


@router.websocket("/voice/{session_id}")
async def voice_websocket(
    websocket: WebSocket,
    session_id: str,
    token: str = Query(default=""),
):
    """
    WebSocket endpoint for real-time voice communication.

    Connect: ws://host/v1/kid/voice/{session_id}?token=<child_jwt>

    Messages from client:
      {type: "start"}              - Initialize session
      {type: "audio", audio: "b64"} - Send PCM16 24kHz mono audio
      {type: "text", text: "..."}  - Send text message
      {type: "end"}                - End session

    Messages to client:
      {type: "status", message: "..."}
      {type: "transcript", role: "user"|"assistant", text: "..."}
      {type: "audio", audio: "b64_wav"}
      {type: "error", message: "..."}
    """
    # Authenticate
    child_id = _verify_child_token(token)
    if not child_id:
        await websocket.close(code=4001, reason="Invalid token")
        return

    await websocket.accept()

    session = VoiceSession(
        session_id=session_id,
        child_id=child_id,
        ws=websocket,
    )

    # Enrich session with child profile + curriculum context from DB
    await _enrich_session(session)

    mode = settings.voice_mode
    mode_labels = {
        "realtime": "OpenAI Realtime API",
        "azure": "Azure OpenAI Realtime API",
        "http": "HTTP (Legacy Pipeline)",
    }
    logger.info(
        f"Voice session started: {session_id} child={child_id} "
        f"name={session.child_name} age={session.child_age} "
        f"type={session.session_type} mode={mode_labels.get(mode, mode)}"
    )

    # Personalized greeting
    greeting = f"캡틴 {session.child_name}! 포포와 루나가 기다리고 있었어!" if session.child_name else "캡틴! 포포와 루나가 기다리고 있었어!"
    await send_msg(websocket, {
        "type": "status",
        "message": greeting,
    })

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "start":
                # R0: Send mission call with theme info
                theme = _get_mission_theme(session)
                name = session.child_name or "캡틴"

                if theme["mission_call"]:
                    await send_msg(websocket, {
                        "type": "mission_call",
                        "text": theme["mission_call"],
                        "missionCode": theme["code"],
                        "ritualPhrase": theme["ritual_phrase"],
                        "closingPhrase": theme["closing_phrase"],
                    })
                else:
                    await send_msg(websocket, {
                        "type": "status",
                        "message": "모험을 시작합니다!",
                    })

                # R3: Send mood check-in only for free_talk sessions
                # (curriculum sessions already got mood check in KidHome free_talk)
                if session.session_type == "free_talk":
                    await send_msg(websocket, {
                        "type": "mood_checkin",
                        "message": f"{name} 캡틴! 오늘 기분은 어때?\n1: 조금 피곤해 😔\n2: 그냥 보통 😊\n3: 기분 좋아! 🤩",
                    })

                # For curriculum sessions, the intro narrator script already
                # ends with Popo's speech prompt (e.g. "'I like...' 말해봐!").
                # Do NOT auto-trigger an opening turn — wait for the child to speak first.
                # The AI will respond using the intro context injected via story_content.

            elif msg_type == "text":
                text = data.get("text", "").strip()
                if not text:
                    continue

                # Check for safety pass signal before AI processing
                signal = interpret_signal(text, session.silence_count, session.turn_count)
                if signal.safety_pass:
                    await send_msg(websocket, {
                        "type": "safety_pass",
                        "text": "알겠어, 캡틴! 포포가 도와줄게~",
                    })

                if mode == "realtime":
                    await handle_realtime_text(session, text)
                elif mode == "azure":
                    content = [{"type": "input_text", "text": text}]
                    session.add_message("user", text)
                    await send_msg(websocket, {
                        "type": "transcript",
                        "role": "user",
                        "text": text,
                    })
                    await handle_azure_session(session, content)
                else:
                    await handle_http_text(session, text)

                # Check if goal was just achieved
                if session.goal_achieved and not getattr(session, '_goal_sent', False):
                    await send_msg(websocket, {
                        "type": "goal_achieved",
                        "text": "미션 성공! 목표 표현을 달성했어요!",
                        "keyExpression": session.key_expression,
                    })
                    session._goal_sent = True

            elif msg_type == "audio":
                audio_b64 = data.get("audio", "")
                if not audio_b64:
                    continue

                if len(audio_b64) > MAX_AUDIO_BASE64_LEN:
                    await send_msg(websocket, {
                        "type": "error",
                        "message": "오디오가 너무 길어요. 짧게 말해 주세요!",
                    })
                    continue

                # Store websocket ref for post-STT safety_pass check
                _prev_history_len = len(session.history)

                if mode == "realtime":
                    await handle_realtime_audio(session, audio_b64)
                elif mode == "azure":
                    await handle_azure_audio(session, audio_b64)
                else:
                    await handle_http_audio(session, audio_b64)

                # Check if goal was just achieved
                if session.goal_achieved and not getattr(session, '_goal_sent', False):
                    await send_msg(websocket, {
                        "type": "goal_achieved",
                        "text": "미션 성공! 목표 표현을 달성했어요!",
                        "keyExpression": session.key_expression,
                    })
                    session._goal_sent = True

                # After audio processing, check if the STT result triggered safety_pass
                if len(session.history) > _prev_history_len:
                    last_user = None
                    for msg in reversed(session.history):
                        if msg["role"] == "user":
                            last_user = msg["text"]
                            break
                    if last_user:
                        sig = interpret_signal(last_user)
                        if sig.safety_pass:
                            await send_msg(websocket, {
                                "type": "safety_pass",
                                "text": "알겠어, 캡틴! 포포가 도와줄게~",
                            })

            elif msg_type == "mood":
                # R3 Emotion Check-in response from frontend
                score = data.get("score", 0)
                if score in (1, 2, 3):
                    session.mood_score = score
                    logger.info(f"Mood check-in: {session_id} score={score}")

            elif msg_type == "end":
                logger.info(f"Voice session ending: {session_id}")
                # Trigger R4 Closing Ritual via AI response
                session.session_ending = True
                closing_text = "세션을 마무리해줘"
                if mode == "realtime":
                    await handle_realtime_text(session, closing_text)
                elif mode == "azure":
                    content = [{"type": "input_text", "text": closing_text}]
                    session.add_message("user", closing_text)
                    await handle_azure_session(session, content)
                else:
                    await handle_http_text(session, closing_text)

                # Send closing ritual UI event
                theme = _get_mission_theme(session)
                await send_msg(websocket, {
                    "type": "closing_ritual",
                    "text": theme["closing_phrase"],
                })
                break

    except WebSocketDisconnect:
        logger.info(f"Voice session disconnected: {session_id}")
    except Exception as e:
        logger.error(f"Voice session error: {session_id} - {e}", exc_info=True)
        try:
            await send_msg(websocket, {
                "type": "error",
                "message": "연결 오류가 발생했습니다.",
            })
        except Exception:
            pass
