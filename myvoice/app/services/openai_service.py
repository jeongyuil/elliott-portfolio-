
import io
from openai import AsyncOpenAI
import json
import random
from app.config import get_settings

settings = get_settings()
# Initialize client only if API key is present to avoid immediate errors on startup if key is missing
# (Though config validation might catch it, it's safer to handle gracefully or let it fail when called)
client = AsyncOpenAI(api_key=settings.openai_api_key)


async def transcribe_audio(audio_bytes: bytes, language: str = "en") -> dict:
    """Whisper STT: Convert audio to text"""
    # Create a file-like object with a name, as OpenAI API expects a file tuple (name, content, type)
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.webm"
    
    transcript = await client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language=language,
        response_format="verbose_json",  # Includes segments and duration
    )
    
    # verbose_json returns an object with text, language, duration, etc.
    return {
        "text": transcript.text,
        "language": transcript.language,
        "duration": transcript.duration,
        "segments": transcript.segments if hasattr(transcript, 'segments') else [],
    }


async def chat_with_ai(
    system_prompt: str,
    conversation_history: list[dict],
    child_utterance: str,
    json_mode: bool = False,
    model: str = "gpt-4o",
) -> str:
    """GPT-4o: Generate conversational AI response"""
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": child_utterance})
    
    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500,
    }
    
    if json_mode:
        kwargs["response_format"] = { "type": "json_object" }

    try:
        response = await client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error("OpenAI chat API failed: %s", e, exc_info=True)
        raise


def mock_chat_response(sys_prompt: str, user_input: str, json_mode: bool) -> str:
    """Fallback when OpenAI is down"""
    text = "Great job! Tell me more."
    feedback = {"type": "good", "skill": "confidence", "level": 3, "message": "Good loud voice!"}
    
    u = user_input.lower()
    if "dog" in u:
        text = "Yes! It is a puppy. What sound does it make?"
        feedback["message"] = "Correct vocabulary!"
        feedback["skill"] = "vocabulary"
    elif "cat" in u:
        text = "Meow! That is a cat. Can you see its tail?"
    elif "lion" in u:
        text = "Roar! The lion is strong."
    elif "bear" in u:
        text = "The bear loves honey."
    elif "hello" in u:
        text = "Hello there! Are you ready for an adventure?"
        
    if json_mode:
        return json.dumps({
            "response_text": text,
            "feedback": feedback
        })
    return text


async def text_to_speech(text: str, voice: str = "nova", response_format: str = "mp3") -> bytes:
    """TTS: Convert text to Audio"""
    response = await client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format=response_format,
    )
    
    # response.content contains the binary audio data
    return response.content
