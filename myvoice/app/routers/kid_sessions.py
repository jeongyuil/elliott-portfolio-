"""Kid-scoped sessions router: start, utterance, end.
Only accessible with child_token (scope=kid).
"""
import uuid
import base64
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Header, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import json
import asyncio

from app.database import get_db
from app.models import Session, Utterance, CurriculumUnit, Activity
from app.models.family import Child
from app.schemas.session import (
    SessionStartRequest,
    SessionStartResponse,
    UtteranceResponse,
    UtteranceUploadRequest,
    TTSRequest,
    SessionEndResponse,
    ActivityInfo,
)
from app.core.security import get_current_child_id
from app.services import speech_pipeline, session_orchestrator
from app.services.safety_filter import filter_input, filter_output
from app.services.openai_service import text_to_speech as legacy_tts
from app.services.conversation_manager import build_system_prompt, get_conversation_history



router = APIRouter()

logger = logging.getLogger("app.routers.kid_sessions")

# ---------------------------------------------------------------------------
# Start session
# ---------------------------------------------------------------------------


from app.core.rate_limit import limiter
from fastapi import Request

# Initialize business logger
business_logger = logging.getLogger("app.business")

@router.post("", response_model=SessionStartResponse, status_code=201)
@limiter.limit("10/minute")
async def start_session(
    req: SessionStartRequest,
    request: Request,
    child_id: str = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db),
):
    """Kids View: Start a learning session (Adventure)"""
    from app.services.curriculum_engine import CurriculumEngine
    from app.models.session import SessionActivity

    target_unit_id = req.curriculum_unit_id
    target_activities = []

    # 1. Determine activities
    if req.curriculum_unit_id:
        # Manual selection
        stmt = select(Activity).where(
            Activity.curriculum_unit_id == req.curriculum_unit_id
        ).order_by(Activity.activity_id)
        result = await db.execute(stmt)
        target_activities = result.scalars().all()
    else:
        # Automatic selection via CurriculumEngine
        engine = CurriculumEngine(db)
        next_activity = await engine.get_next_activity(child_id)
        
        if next_activity:
            target_activities = [next_activity]
            target_unit_id = next_activity.curriculum_unit_id

    # 2. Create Session
    session = Session(
        child_id=uuid.UUID(child_id),
        session_type=req.session_type,
        curriculum_unit_id=target_unit_id,
        status="active",
    )
    db.add(session)
    await db.flush()

    # 3. Create SessionActivity records
    for i, activity in enumerate(target_activities):
        session_activity = SessionActivity(
            session_id=session.session_id,
            activity_id=activity.activity_id,
            order_index=i,
            status="pending"
        )
        db.add(session_activity)

    await db.commit()

    # Initialise Redis state for this session
    session_id_str = str(session.session_id)
    await session_orchestrator.create_session_state(session_id_str)
    await session_orchestrator.transition_state(session_id_str, "active")

    # [METRIC] Log Session Start
    business_logger.info(
        "Session Started",
        extra={
            "event": "session_start",
            "session_id": session_id_str,
            "child_id": child_id,
            "unit_id": target_unit_id,
            "activity_count": len(target_activities)
        }
    )

    return SessionStartResponse(
        session_id=session.session_id,
        child_id=session.child_id,
        session_type=session.session_type,
        status=session.status,
        start_time=session.start_time,
        curriculum_unit_id=target_unit_id,
        activities=[
            ActivityInfo(
                activity_id=a.activity_id,
                name=a.name,
                activity_type=a.activity_type,
                intro_narrator_script=a.intro_narrator_script,
                outro_narrator_script=a.outro_narrator_script,
                estimated_duration_minutes=a.estimated_duration_minutes,
                image_path=a.image_path,
            ) for a in target_activities
        ],
    )


# ---------------------------------------------------------------------------
# Utterance — Phase-aware pipeline
# ---------------------------------------------------------------------------

@router.post("/{session_id}/utterances", response_model=UtteranceResponse)
@limiter.limit("30/minute")
async def upload_utterance(
    session_id: uuid.UUID,
    req: UtteranceUploadRequest,
    request: Request,
    background_tasks: BackgroundTasks,  # Added BackgroundTasks
    x_idempotency_key: str = Header(..., alias="X-Idempotency-Key"),
    child_id: str = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db),
):
    import time
    start_ts = time.time()
    """Kids View: Process child voice → STT → Safety → LLM → Safety → TTS"""
    logger.info(f"Received utterance upload request for session {session_id}")

    # 1. Verify active DB session
    result = await db.execute(
        select(Session).where(
            Session.session_id == session_id,
            Session.child_id == uuid.UUID(child_id),
            Session.status == "active",
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Active session not found")

    # 2. Idempotency check
    existing = await db.execute(
        select(Utterance).where(
            Utterance.session_id == session_id,
            Utterance.idempotency_key == x_idempotency_key,
            Utterance.speaker_type == "child",
        )
    )
    existing_child = existing.scalar_one_or_none()
    if existing_child:
        ai_result = await db.execute(
            select(Utterance).where(
                Utterance.session_id == session_id,
                Utterance.turn_index == existing_child.turn_index + 1,
                Utterance.speaker_type == "ai",
            )
        )
        ai_cached = ai_result.scalar_one_or_none()
        if ai_cached:
            return UtteranceResponse(
                utterance_id=ai_cached.utterance_id,
                child_text=existing_child.text_raw,
                ai_response_text=ai_cached.text_raw,
                ai_response_audio_base64=None,
                turn_index=ai_cached.turn_index,
                speaker_type="ai",
                text_transcript=ai_cached.text_raw,
                feedback=None,
            )

    # 3. Decode audio / text
    child_text = ""
    stt_engine_used = "whisper-1"
    stt_result = None

    if req.text_input:
        child_text = req.text_input
        stt_engine_used = "browser-stt"
        stt_is_empty = not child_text.strip()
        stt_confidence = 1.0
    elif req.audio_data:
        audio_bytes = base64.b64decode(req.audio_data)
        stt_result = await speech_pipeline.speech_to_text(audio_bytes, language="auto")
        child_text = stt_result.text
        stt_engine_used = "whisper-1"
        stt_is_empty = stt_result.is_empty
        stt_confidence = stt_result.confidence
    else:
        raise HTTPException(status_code=400, detail="Either audio_data or text_input required")

    session_id_str = str(session_id)

    # 4. Handle silence / empty audio
    if stt_is_empty:
        silence_event = await session_orchestrator.handle_silence(session_id_str)
        reprompt = silence_event.reprompt_text or "무슨 말인지 못 들었어! 다시 말해줄래? 🐾"
        try:
            tts_audio = await speech_pipeline.text_to_speech(reprompt, character="popo")
            tts_b64 = base64.b64encode(tts_audio).decode()
        except Exception: tts_b64 = None
        return UtteranceResponse(
            utterance_id=uuid.uuid4(), child_text="", ai_response_text=reprompt,
            ai_response_audio_base64=tts_b64, turn_index=0, speaker_type="ai",
            text_transcript=reprompt, feedback=None, next_phase="transition",
        )

    # 5. Safety filter
    input_safety = filter_input(child_text)
    if not input_safety.is_safe:
        child_text = input_safety.safe_text

    # 6. Load current session phase
    state_data = await session_orchestrator.get_session_state(session_id_str)
    current_phase = state_data.phase if state_data else "interactive"

    # 7-8. Phase Transitions — skip transition, go straight to interactive
    if current_phase in ("narrator_intro", "transition"):
        await session_orchestrator.advance_phase(session_id_str, "interactive")
        current_phase = "interactive"

    # 9. Phase 3 (interactive): full pipeline
    existing_count = await db.execute(select(func.count(Utterance.utterance_id)).where(Utterance.session_id == session_id))
    turn_index = existing_count.scalar() or 0

    # Context (Since session is already verified, we can use session.curriculum_unit_id)
    unit = None
    activity = None
    if session.curriculum_unit_id:
        unit = (await db.execute(select(CurriculumUnit).where(CurriculumUnit.curriculum_unit_id == session.curriculum_unit_id))).scalar_one_or_none()
        if req.activity_id:
            activity = (await db.execute(select(Activity).where(Activity.activity_id == req.activity_id))).scalar_one_or_none()
        elif unit:
            activity = (await db.execute(select(Activity).where(Activity.curriculum_unit_id == session.curriculum_unit_id).limit(1))).scalar_one_or_none()

    # Load child profile for prompt personalization
    child = await db.get(Child, child_id)
    child_name = child.name if child else ""
    child_age = 7
    child_level = child.level if child else 1
    if child and child.birth_date:
        from datetime import date as _date
        bd = child.birth_date
        if hasattr(bd, 'date'):
            bd = bd.date()
        today = _date.today()
        child_age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))

    system_prompt = build_system_prompt(
        unit, activity,
        child_name=child_name, child_age=child_age, child_level=child_level,
    )
    conversation_history = await get_conversation_history(db, session_id)

    # 10. LLM
    ctx = speech_pipeline.ConversationContext(child_text=child_text, system_prompt=system_prompt, history=conversation_history, character="luna")
    try:
        llm_start = time.time()
        dialogue = await speech_pipeline.generate_dialogue(ctx)
        logger.info(f"LLM Duration: {time.time() - llm_start:.2f}s")
        ai_text = dialogue.text
        feedback_data = dialogue.feedback
    except Exception:
        ai_text = "Great! Keep going! 🌟"
        feedback_data = None

    # 11. Safety filter — AI output
    output_safety = filter_output(ai_text)
    ai_text = output_safety.safe_text if not output_safety.is_safe else ai_text

    # 12. TTS
    try:
        tts_start = time.time()
        tts_audio = await speech_pipeline.text_to_speech(ai_text, character="luna")
        logger.info(f"TTS Duration: {time.time() - tts_start:.2f}s")
        tts_b64 = base64.b64encode(tts_audio).decode()
    except Exception:
        tts_b64 = None

    # 13. Metrics & Persistence
    await session_orchestrator.reset_silence_counter(session_id_str)
    child_utterance = Utterance(
        session_id=session_id, turn_index=turn_index, speaker_type="child", utterance_id=uuid.uuid4(),
        text_raw=child_text, language=getattr(stt_result, "language", "en") if stt_result else "unknown",
        stt_engine=stt_engine_used, stt_confidence=stt_confidence, idempotency_key=x_idempotency_key,
    )
    ai_utterance = Utterance(session_id=session_id, turn_index=turn_index + 1, speaker_type="ai", utterance_id=uuid.uuid4(), text_raw=ai_text, language="mixed")
    db.add(child_utterance); db.add(ai_utterance)
    await db.commit()
    
    from app.services.evaluation_service import evaluate_utterance
    background_tasks.add_task(evaluate_utterance, child_utterance.utterance_id)

    return UtteranceResponse(
        utterance_id=ai_utterance.utterance_id, child_text=child_text, ai_response_text=ai_text,
        ai_response_audio_base64=tts_b64, turn_index=turn_index + 1, speaker_type="ai",
        text_transcript=ai_text, feedback=feedback_data, next_phase="interactive",
    )


# ---------------------------------------------------------------------------
# TTS endpoint (standalone)
# ---------------------------------------------------------------------------

@router.post("/{session_id}/tts")
async def generate_session_tts(
    session_id: str,
    request: TTSRequest,
    _child_id: str = Depends(get_current_child_id),
):
    character = getattr(request, "character", "luna")
    try:
        if character == "multi":
            audio_bytes = await speech_pipeline.multi_character_tts(request.text)
        else:
            audio_bytes = await speech_pipeline.text_to_speech(request.text, character=character)
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        return {"audio_base64": audio_base64}
    except Exception:
        logger.exception("TTS generation failed")
        raise HTTPException(status_code=502, detail="TTS generation failed")


# ---------------------------------------------------------------------------
# End session
# ---------------------------------------------------------------------------

@router.post("/{session_id}/end", response_model=SessionEndResponse)
async def end_session(
    session_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    child_id: str = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db),
):
    """Kids View: End the session"""
    result = await db.execute(
        select(Session).where(
            Session.session_id == session_id,
            Session.child_id == uuid.UUID(child_id),
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.status = "ended"
    session.end_time = datetime.now(timezone.utc)

    duration = 0
    if session.start_time:
        duration = int((session.end_time - session.start_time).total_seconds())
    session.duration_seconds = duration

    count_stmt = select(func.count(Utterance.utterance_id)).where(Utterance.session_id == session_id)
    turn_count = (await db.execute(count_stmt)).scalar() or 0

    # Mark SessionActivities as completed
    # For now, mark all activities in this session as completed if turn_count > 0
    # In future, we might want granular control per activity if multiple are in one session
    from app.models.session import SessionActivity
    if turn_count > 0:
        await db.execute(
            select(SessionActivity)
            .where(SessionActivity.session_id == session_id)
        )
        # We can't use update() with join easily in async, so let's just fetch and update
        # Actually, simpler:
        # UPDATE session_activities SET status='completed', ended_at=NOW() WHERE session_id=...
        from sqlalchemy import update
        await db.execute(
            update(SessionActivity)
            .where(SessionActivity.session_id == session_id)
            .values(status="completed", ended_at=datetime.now(timezone.utc))
        )

    await db.commit()

    # Transition Redis state to ended
    try:
        await session_orchestrator.transition_state(str(session_id), "ended")
    except Exception:
        pass  # Non-critical: Redis state cleanup

    # 4. Award XP (Gamification Service)
    from app.services.gamification_service import GamificationService
    xp_amount = GamificationService.calculate_session_xp(duration, turn_count)
    xp_result = await GamificationService.award_xp(db, child_id, xp_amount, "session_complete")
    
    # Trigger Skill Calculation in Background
    from app.services.skill_service import calculate_skill_levels
    background_tasks.add_task(calculate_skill_levels, child_id)
    
    # [METRIC] Log Session Start
    business_logger.info(
        "Session Ended",
        extra={
            "event": "session_end",
            "session_id": str(session_id),
            "child_id": child_id,
            "duration_sec": duration,
            "total_turns": turn_count,
            "xp_earned": xp_result["earned_xp"]
        }
    )

    return SessionEndResponse(
        duration_seconds=duration,
        engagement_score=session.engagement_score,
        total_turns=turn_count,
        earned_xp=xp_result["earned_xp"], # Added field
        new_level=xp_result["level"],      # Added field
        level_up=xp_result["level_up"]     # Added field
    )
