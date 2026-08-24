"""
Voice Proxy Service - bridges frontend WebSocket to AI voice pipeline.

Supports three modes via VOICE_MODE config:
  - "realtime": OpenAI Realtime API (movice pattern - single connection for STT+LLM+TTS)
  - "azure": Azure OpenAI Realtime API
  - "http": Legacy fallback using Whisper STT + GPT-4 + TTS pipeline (3 separate calls)

Protocol (Frontend <-> Backend):
  Frontend -> Backend:
    {type: "start"}
    {type: "audio", audio: "<base64_pcm16_24k_mono>"}
    {type: "text", text: "..."}
    {type: "end"}

  Backend -> Frontend:
    {type: "status", message: "..."}
    {type: "transcript", role: "user"|"assistant", text: "..."}
    {type: "audio", audio: "<base64_wav>"}
    {type: "error", message: "..."}
"""
import base64
import io
import logging
import re
import wave
from dataclasses import dataclass, field
from fastapi import WebSocket

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

SAMPLE_RATE = 24000
CHANNELS = 1

# Marker injected by LLM when child achieves the key_expression goal
GOAL_MARKER = "[GOAL_ACHIEVED]"


@dataclass
class VoiceSession:
    """Manages a single voice conversation session."""
    session_id: str
    child_id: str
    ws: WebSocket
    history: list = field(default_factory=list)

    # Enriched context (loaded from DB on session start)
    child_name: str = ""
    child_age: int = 7
    child_language: str = "ko"
    child_level: int = 1

    # Curriculum context
    session_type: str = "free_talk"
    unit_title: str = ""
    unit_description: str = ""
    unit_week: int = 0
    difficulty_level: int = 1
    korean_ratio: int = 50
    target_skills: list = field(default_factory=list)

    # Activity context
    activity_name: str = ""
    activity_type: str = ""
    instructions_for_ai: str = ""
    story_content: str = ""
    key_expression: str = ""
    intro_narrator_script: str = ""
    outro_narrator_script: str = ""

    # Story theme
    story_theme: str = "earth_crew"

    # Session state
    phase: str = "interactive"
    turn_count: int = 0
    silence_count: int = 0
    goal_achieved: bool = False  # True after child says the key_expression

    # Relationship state
    mood_score: int = 0           # 0=not asked, 1=low, 2=normal, 3=high (R3)
    session_ending: bool = False  # True when "end" message received

    def add_message(self, role: str, text: str):
        self.history.append({"role": role, "text": text})
        self.turn_count += 1


def pcm16_to_wav(pcm_bytes: bytes) -> bytes:
    """Convert raw PCM16 24kHz mono to WAV bytes."""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm_bytes)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Character segment parsing & per-character TTS
# ---------------------------------------------------------------------------

TAG_RE = re.compile(r'\[(나레이션|포포|루나)\]\s*')

CHARACTER_VOICES = {
    "narrator": "nova",     # 동화 내레이터 — 따뜻하고 부드러운 목소리
    "popo": "fable",        # 포포 — 표현력 풍부한 따뜻한 코치
    "luna": "shimmer",      # 루나 — 밝고 친근한 영어 캐릭터
}

TAG_TO_KEY = {"나레이션": "narrator", "포포": "popo", "루나": "luna"}


def parse_character_segments(text: str) -> list[tuple[str, str]]:
    """
    Parse AI response into (character_key, dialogue_text) segments.
    E.g. "[나레이션] 숲 속에서... [루나] Wow! [포포] 캡틴!" →
      [("narrator", "숲 속에서..."), ("luna", "Wow!"), ("popo", "캡틴!")]
    """
    segments: list[tuple[str, str]] = []
    last_idx = 0
    last_key = "popo"  # default if no tag

    for m in TAG_RE.finditer(text):
        before = text[last_idx:m.start()].strip()
        if before:
            segments.append((last_key, before))
        last_key = TAG_TO_KEY.get(m.group(1), "popo")
        last_idx = m.end()

    remaining = text[last_idx:].strip()
    if remaining:
        segments.append((last_key, remaining))

    if not segments and text.strip():
        segments.append(("popo", text.strip()))

    return segments


async def _tts_for_character(text: str, character: str) -> bytes:
    """Generate TTS audio for a specific character voice using OpenAI TTS API."""
    import openai

    client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    voice = CHARACTER_VOICES.get(character, "shimmer")

    response = await client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="wav",
    )
    return response.content


AUDIO_CHUNK_SIZE = 512 * 1024  # 512KB per chunk (well under 1MB WS default)


async def send_msg(ws: WebSocket, msg: dict):
    """Send JSON message to frontend WebSocket."""
    await ws.send_json(msg)


async def send_audio_chunked(ws: WebSocket, wav_bytes: bytes):
    """Send audio in chunks to avoid WebSocket frame size limits."""
    b64 = base64.b64encode(wav_bytes).decode()
    if len(b64) <= AUDIO_CHUNK_SIZE:
        await ws.send_json({"type": "audio", "audio": b64})
    else:
        total = len(b64)
        idx = 0
        chunk_num = 0
        while idx < total:
            chunk = b64[idx:idx + AUDIO_CHUNK_SIZE]
            await ws.send_json({
                "type": "audio_chunk",
                "audio": chunk,
                "chunk": chunk_num,
                "final": idx + AUDIO_CHUNK_SIZE >= total,
            })
            idx += AUDIO_CHUNK_SIZE
            chunk_num += 1


# ---------------------------------------------------------------------------
# Chat Completions + per-character TTS (replaces Realtime API for text gen)
# ---------------------------------------------------------------------------

async def _chat_completion_and_tts(session: VoiceSession):
    """
    Generate AI response via Chat Completions API, then TTS per character.

    Uses gpt-4o-mini for fast text generation, then parses [나레이션]/[포포]/[루나]
    tags and generates TTS with different voices for each character.
    """
    import openai

    client = openai.AsyncOpenAI(api_key=settings.openai_api_key)

    # Build messages from history (caller already added user message)
    messages = [{"role": "system", "content": _build_instructions(session)}]
    for record in session.history:
        messages.append({"role": record["role"], "content": record["text"]})

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        full_transcript = response.choices[0].message.content or ""
    except Exception as e:
        logger.error(f"Chat Completion error: {e}", exc_info=True)
        await send_msg(session.ws, {
            "type": "error",
            "message": "AI 응답 처리 중 오류가 발생했습니다.",
        })
        return

    if not full_transcript:
        return

    # Detect and strip goal achievement marker before TTS
    if GOAL_MARKER in full_transcript:
        full_transcript = full_transcript.replace(GOAL_MARKER, "").strip()
        session.goal_achieved = True
        logger.info(f"Goal achieved detected in session {session.session_id}")

    logger.info(f"AI response: {full_transcript[:200]}...")
    session.add_message("assistant", full_transcript)

    # Send full transcript to frontend (for chat bubble rendering)
    await send_msg(session.ws, {
        "type": "transcript",
        "role": "assistant",
        "text": full_transcript,
    })

    # Per-character TTS — parse segments, generate audio for each voice
    segments = parse_character_segments(full_transcript)
    for char_key, dialogue in segments:
        try:
            tts_bytes = await _tts_for_character(dialogue, char_key)
            await send_audio_chunked(session.ws, tts_bytes)
        except Exception as e:
            logger.error(f"TTS failed for {char_key}: {e}")


async def handle_realtime_text(session: VoiceSession, text: str):
    """Process text input: Chat Completions → per-character TTS."""
    session.add_message("user", text)
    await send_msg(session.ws, {
        "type": "transcript",
        "role": "user",
        "text": text,
    })

    await _chat_completion_and_tts(session)


async def handle_realtime_audio(session: VoiceSession, audio_base64: str):
    """Process audio input: Whisper STT → Chat Completions → per-character TTS."""
    import openai

    client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    audio_bytes = base64.b64decode(audio_base64)

    # Whisper STT for user transcript display
    wav_bytes = pcm16_to_wav(audio_bytes)
    try:
        transcription = await client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", wav_bytes, "audio/wav"),
        )
        user_text = transcription.text
        logger.info(f"STT result: {user_text}")
    except Exception as e:
        logger.error(f"Whisper STT failed: {e}")
        user_text = ""

    if not user_text or not user_text.strip():
        await send_msg(session.ws, {
            "type": "transcript",
            "role": "user",
            "text": "(소리가 감지되지 않았어요)",
        })
        return

    # Send user transcript to frontend
    session.add_message("user", user_text)
    await send_msg(session.ws, {
        "type": "transcript",
        "role": "user",
        "text": user_text,
    })

    # Chat Completions + per-character TTS
    await _chat_completion_and_tts(session)


# ---------------------------------------------------------------------------
# Azure OpenAI Realtime API mode
# ---------------------------------------------------------------------------

async def handle_azure_session(session: VoiceSession, content: list[dict]):
    """Process a single turn using Azure OpenAI Realtime API."""
    from openai import AsyncAzureOpenAI

    client = AsyncAzureOpenAI(
        api_key=settings.azure_realtime_api_key,
        api_version=settings.azure_realtime_api_version,
        azure_endpoint=settings.azure_realtime_endpoint,
    )

    async with client.realtime.connect(
        model=settings.azure_realtime_deployment,
    ) as connection:
        # Load conversation history
        for record in session.history:
            content_type = "input_text" if record["role"] == "user" else "text"
            await connection.conversation.item.create(
                item={
                    "type": "message",
                    "role": record["role"],
                    "content": [{"type": content_type, "text": record["text"]}],
                }
            )

        # Configure session — TEXT only (TTS done per-character)
        await connection.session.update(session={
            "modalities": ["text"],
            "temperature": 0.7,
            "instructions": _build_instructions(session),
            "turn_detection": None,
            "input_audio_transcription": {"model": "whisper-1"},
        })

        # Send user content
        await connection.conversation.item.create(
            item={
                "type": "message",
                "role": "user",
                "content": content,
            }
        )

        # Request response
        await connection.response.create()

        # Stream response (text only)
        full_transcript = ""

        async for event in connection:
            if event.type == "response.text.delta":
                full_transcript += event.delta

            elif event.type == "response.text.done":
                break

            elif event.type == "response.done":
                break

            elif event.type == "error":
                logger.error(f"Realtime API error: {event.error}")
                await send_msg(session.ws, {
                    "type": "error",
                    "message": "AI 응답 처리 중 오류가 발생했습니다.",
                })
                return

    if not full_transcript:
        return

    # Detect and strip goal achievement marker before TTS
    if GOAL_MARKER in full_transcript:
        full_transcript = full_transcript.replace(GOAL_MARKER, "").strip()
        session.goal_achieved = True
        logger.info(f"Goal achieved detected in session {session.session_id} (azure)")

    logger.info(f"AI response (azure): {full_transcript[:200]}...")
    session.add_message("assistant", full_transcript)
    await send_msg(session.ws, {
        "type": "transcript",
        "role": "assistant",
        "text": full_transcript,
    })

    # Per-character TTS
    segments = parse_character_segments(full_transcript)
    for char_key, dialogue in segments:
        try:
            tts_bytes = await _tts_for_character(dialogue, char_key)
            await send_audio_chunked(session.ws, tts_bytes)
        except Exception as e:
            logger.error(f"TTS failed for {char_key}: {e}")


async def handle_azure_audio(session: VoiceSession, audio_base64: str):
    """Azure Realtime mode: STT via Azure Whisper, then Realtime API."""
    from openai import AsyncAzureOpenAI

    audio_bytes = base64.b64decode(audio_base64)
    wav_bytes = pcm16_to_wav(audio_bytes)

    whisper_client = AsyncAzureOpenAI(
        api_key=settings.azure_whisper_api_key or settings.azure_realtime_api_key,
        api_version=settings.azure_whisper_api_version,
        azure_endpoint=settings.azure_whisper_endpoint or settings.azure_realtime_endpoint,
    )

    transcription = await whisper_client.audio.transcriptions.create(
        model=settings.azure_whisper_deployment,
        file=("audio.wav", wav_bytes, "audio/wav"),
    )
    user_text = transcription.text
    logger.info(f"STT result: {user_text}")

    session.add_message("user", user_text)
    await send_msg(session.ws, {
        "type": "transcript",
        "role": "user",
        "text": user_text,
    })

    content = [{"type": "input_text", "text": user_text}]
    await handle_azure_session(session, content)


# ---------------------------------------------------------------------------
# HTTP fallback mode (Whisper + GPT-4 + TTS - 3 separate calls)
# ---------------------------------------------------------------------------

async def handle_http_text(session: VoiceSession, text: str):
    """HTTP fallback: use existing speech pipeline for text input."""
    from app.services.speech_pipeline import (
        generate_dialogue,
        text_to_speech,
        ConversationContext,
    )

    session.add_message("user", text)
    await send_msg(session.ws, {
        "type": "transcript",
        "role": "user",
        "text": text,
    })

    ctx = ConversationContext(
        child_text=text,
        system_prompt=_build_instructions(session),
        history=[{"role": m["role"], "content": m["text"]} for m in session.history[:-1]],
        character="popo",
    )

    result = await generate_dialogue(ctx)
    response_text = result.text
    if isinstance(response_text, dict):
        response_text = response_text.get("text", response_text.get("response", str(response_text)))
    response_text = str(response_text)

    # Detect and strip goal achievement marker before TTS
    if GOAL_MARKER in response_text:
        response_text = response_text.replace(GOAL_MARKER, "").strip()
        session.goal_achieved = True
        logger.info(f"Goal achieved detected in session {session.session_id} (http)")

    session.add_message("assistant", response_text)

    await send_msg(session.ws, {
        "type": "transcript",
        "role": "assistant",
        "text": response_text,
    })

    # Per-character TTS
    segments = parse_character_segments(response_text)
    for char_key, dialogue in segments:
        try:
            tts_bytes = await _tts_for_character(dialogue, char_key)
            await send_audio_chunked(session.ws, tts_bytes)
        except Exception as e:
            logger.error(f"TTS failed for {char_key}: {e}")


async def handle_http_audio(session: VoiceSession, audio_base64: str):
    """HTTP fallback: use existing speech pipeline for audio input."""
    from app.services.speech_pipeline import speech_to_text

    raw_bytes = base64.b64decode(audio_base64)
    audio_bytes = pcm16_to_wav(raw_bytes)
    stt_result = await speech_to_text(audio_bytes)

    if stt_result.is_empty:
        await send_msg(session.ws, {
            "type": "transcript",
            "role": "user",
            "text": "(소리가 감지되지 않았어요)",
        })
        return

    await handle_http_text(session, stt_result.text)


# ---------------------------------------------------------------------------
# System instructions (shared by all modes)
# Uses prompt_builder for 3-character system (Luna + Popo + Narrator)
# ---------------------------------------------------------------------------

def _build_instructions(session: VoiceSession) -> str:
    """Build system instructions using the 밤토리 3-character prompt system."""
    from app.services.prompt_builder import SessionContext, build_voice_instructions
    from app.services.signal_interpreter import interpret_signal

    # Build signal from last user message
    child_signal = None
    last_user_msg = None
    for msg in reversed(session.history):
        if msg["role"] == "user":
            last_user_msg = msg["text"]
            break

    if last_user_msg:
        signal = interpret_signal(
            last_user_msg,
            silence_count=session.silence_count,
            turn_count=session.turn_count,
        )
        child_signal = signal.to_dict()

        # Track silence
        if signal.intent == "silence":
            session.silence_count += 1
        else:
            session.silence_count = 0

        # Auto-detect mood score from early turns (R3 response)
        if session.mood_score == 0 and session.turn_count <= 4:
            stripped = last_user_msg.strip()
            if stripped in ("1", "2", "3"):
                session.mood_score = int(stripped)
                logger.info(f"Mood auto-detected from text: {session.mood_score}")

    # Inject intro script as story context so the AI continues from the intro
    story_content = session.story_content
    if not story_content and getattr(session, 'intro_narrator_script', ''):
        story_content = (
            "[직전 인트로에서 아이에게 보여준 내용 — 이 내용을 이어서 진행하세요]\n"
            + session.intro_narrator_script
        )

    ctx = SessionContext(
        child_name=session.child_name,
        child_age=session.child_age,
        child_language=session.child_language,
        child_level=session.child_level,
        unit_title=session.unit_title,
        unit_description=session.unit_description,
        unit_week=session.unit_week,
        difficulty_level=session.difficulty_level,
        korean_ratio=session.korean_ratio,
        target_skills=session.target_skills,
        activity_name=session.activity_name,
        activity_type=session.activity_type,
        instructions_for_ai=session.instructions_for_ai,
        story_content=story_content,
        key_expression=session.key_expression,
        session_type=session.session_type,
        story_theme=session.story_theme,
        phase=session.phase,
        turn_count=session.turn_count,
        silence_count=session.silence_count,
        mood_score=session.mood_score,
        session_ending=session.session_ending,
        goal_achieved=session.goal_achieved,
        child_signal=child_signal,
    )

    return build_voice_instructions(ctx)
