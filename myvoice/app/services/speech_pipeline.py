import os
import base64
import json
import logging
from dataclasses import dataclass
from typing import Optional, List, Dict
import openai
from app.config import get_settings
from app.services.safety_filter import filter_input, filter_output

import hashlib
from redis import asyncio as aioredis

logger = logging.getLogger(__name__)

# Initialize OpenAI
settings = get_settings()
client = openai.AsyncOpenAI(api_key=settings.openai_api_key)

# Initialize Redis
redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", encoding="utf-8", decode_responses=False)

CHARACTER_VOICES = {
    "luna": "nova",
    "popo": "fable",
    "narrator": "onyx"
}


@dataclass
class SttResult:
    text: str
    language: str        # "en" | "ko"
    confidence: float    # 0.0 ~ 1.0 (approximated)
    is_empty: bool       # Noise/Silence detection
    duration_ms: int = 0

@dataclass
class ConversationContext:
    child_text: str
    system_prompt: str
    history: List[Dict[str, str]] # [{"role": "user", "content": "..."}, ...]
    character: str = "luna" # luna | popo
    max_history_turns: int = 10

@dataclass
class DialogueResult:
    text: str
    emotion: str = "neutral"
    feedback: Optional[Dict] = None # {"type": "good", ...}

def _detect_audio_extension(data: bytes) -> str:
    """Detect audio format from magic bytes and return an appropriate file extension."""
    if data[:4] == b'OggS':
        return '.ogg'
    if data[:4] == b'fLaC':
        return '.flac'
    if data[:3] == b'ID3' or data[:2] == b'\xff\xfb':
        return '.mp3'
    if data[4:8] == b'ftyp':
        return '.mp4'
    # Default: webm (Chrome/most browsers)
    return '.webm'


async def speech_to_text(audio_bytes: bytes, language: str = "auto") -> SttResult:
    """
    Convert audio to text using OpenAI Whisper API.
    Handles ephemeral files for the API call.
    """
    import tempfile

    # Check if empty (simple size check — very small files are likely silence)
    if len(audio_bytes) < 200:
         return SttResult("", "unknown", 0.0, True)

    ext = _detect_audio_extension(audio_bytes)
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        # 2. Call Whisper
        # Optimization: Adding a prompt helps Whisper with specific words (토리, 루나)
        # and punctuation. Specifying language reduces detection latency.
        
        with open(tmp_path, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
            )
            
        text = transcript.text.strip()
        detected_lang = getattr(transcript, "language", "unknown")
        
        logger.info(f"STT Whisper Result: '{text}' (lang: {detected_lang})")

        # Calculate approximate confidence from avg_logprob
        import math
        avg_logprob = -10.0
        if hasattr(transcript, 'segments') and transcript.segments:
             try:
                 avg_logprob = sum(s.avg_logprob for s in transcript.segments) / len(transcript.segments)
             except (AttributeError, TypeError):
                 pass
        
        confidence = math.exp(max(avg_logprob, -20.0))
        is_empty = len(text) == 0

        return SttResult(
            text=text,
            language=detected_lang,
            confidence=confidence,
            is_empty=is_empty
        )

    except Exception as e:
        logger.error(f"STT Error: {e}")
        # Fallback?
        return SttResult("", "error", 0.0, True)
        
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


async def generate_dialogue(ctx: ConversationContext) -> DialogueResult:
    """
    Generate dialogue response using GPT-4o-mini.
    Enforces JSON format for structured output (text + emotion + feedback).
    IMPORTANT: System prompt must contain the word 'JSON'.
    """
    # Ensure system prompt mentions JSON to satisfy API requirement
    system_prompt = ctx.system_prompt
    if "json" not in system_prompt.lower():
        system_prompt += " You must respond in valid JSON format."

    messages = [
        {"role": "system", "content": system_prompt},
    ]
    messages.extend(ctx.history)
    messages.append({"role": "user", "content": ctx.child_text})

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=200, 
        )
        
        content = response.choices[0].message.content
        logger.info(f"LLM Raw Response: {content}")
        data = json.loads(content)
        
        return DialogueResult(
            text=data.get("response", data.get("response_text", "")),
            emotion=data.get("emotion", "neutral"),
            feedback=data.get("feedback")
        )

    except Exception as e:
        logger.error(f"LLM Error: {e}")
        return DialogueResult("Sorry, can you say that again?", "confused")


async def generate_dialogue_stream(ctx: ConversationContext):
    """
    Stream dialogue response as it's generated.
    Returns chunks of text (sentences) for faster TTS processing.
    """
    system_prompt = ctx.system_prompt
    if "json" not in system_prompt.lower():
        system_prompt += " You must respond in valid JSON format."

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(ctx.history)
    messages.append({"role": "user", "content": ctx.child_text})

    full_content = ""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=200,
            stream=True, # Enable streaming
        )
        
        async for chunk in response:
            delta = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta.content else ""
            full_content += delta
            # We could potentially yield partial sentences here, 
            # but JSON mode makes streaming partial chunks tricky because it needs to be valid JSON.
            # INSTEAD: For 1.0s target, we should move AWAY from JSON mode for the response text.
            # But the feedback needs JSON.
        
        # For now, let's keep it simple: wait for full JSON but process faster.
        # Wait, if we wait for full JSON, it's not really streaming.
        # TODO: Move to a Custom parser or non-JSON mode for the response part.
        
        data = json.loads(full_content)
        return DialogueResult(
            text=data.get("response", data.get("response_text", "")),
            emotion=data.get("emotion", "neutral"),
            feedback=data.get("feedback")
        )

    except Exception as e:
        logger.error(f"LLM Streaming Error: {e}")
        return DialogueResult("Sorry, can you say that again?", "confused")


async def text_to_speech(text: str, character: str = "luna") -> bytes:
    """
    Convert text to speech using OpenAI TTS.
    Implements Redis caching (TTL 1h).
    """
    # 1. Check Cache
    cache_key = f"tts:{character}:{hashlib.md5(text.encode()).hexdigest()}"
    try:
        cached_audio = await redis.get(cache_key)
        if cached_audio:
            logger.info("TTS Cache Hit")
            return cached_audio # type: ignore
    except Exception as e:
        logger.warning(f"Redis Error: {e}")

    # 2. Call OpenAI TTS
    voice_map = {
        "luna": "shimmer",    # 밝고 친근한 여성 목소리
        "popo": "fable",      # 표현력 풍부한 남성 목소리 (비밀 요원 코치)
        "narrator": "nova",   # 따뜻한 여성 나레이터
    }
    voice = voice_map.get(character, "alloy")
    
    try:
        response = await client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
        )
        audio_bytes = response.content
        
        # 3. Save to Cache (TTL 1 hour)
        try:
            await redis.set(cache_key, audio_bytes, ex=3600)
        except Exception as e:
            logger.warning(f"Redis Set Error: {e}")
            
        return audio_bytes

    except Exception as e:
        logger.error(f"TTS Error: {e}")
        raise e


async def multi_character_tts(text: str) -> bytes:
    """
    Parse [나레이션]/[포포]/[루나] tags and generate TTS for each segment
    with the appropriate voice, then concatenate the audio.
    """
    from app.services.voice_proxy import parse_character_segments

    TAG_TO_CHARACTER = {"narrator": "narrator", "popo": "popo", "luna": "luna"}
    segments = parse_character_segments(text)

    if not segments:
        # No tags found — treat as narrator
        return await text_to_speech(text, character="narrator")

    audio_parts = []
    for key, segment_text in segments:
        character = TAG_TO_CHARACTER.get(key, "narrator")
        try:
            audio = await text_to_speech(segment_text.strip(), character=character)
            audio_parts.append(audio)
        except Exception as e:
            logger.warning(f"Multi-character TTS failed for {character}: {e}")
            continue

    if not audio_parts:
        return await text_to_speech(text, character="narrator")

    # Concatenate MP3 segments (OpenAI TTS returns MP3)
    return b"".join(audio_parts)

