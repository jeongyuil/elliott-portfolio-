import asyncio
import time
import os
import sys

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.openai_service import chat_with_ai, text_to_speech
from app.services.conversation_manager import build_system_prompt

async def test_latency():
    print("🚀 Starting Latency Test...")
    
    # Warm up (optional)
    print("Running warm-up request...")
    try:
        await chat_with_ai("System Prompt", [], "ping")
    except Exception as e:
        print(f"Warm-up failed (expected if no API key or network issue): {e}")

    print("\n--- MEASURING STT (Mocked if file missing) ---")
    stt_duration = 0 # Placeholder
    print(f"STT Duration: {stt_duration:.4f}s (Skipped/Mocked)")

    print("\n--- MEASURING LLM (Chat Completion) ---")
    llm_start = time.time()
    
    # Use the system prompt from conversation_manager
    system_prompt = build_system_prompt(None, None)
    
    user_text = "Hello, I am a child learning English."
    
    ai_text = await chat_with_ai(
        system_prompt=system_prompt,
        conversation_history=[],
        child_utterance=user_text
    )
    llm_end = time.time()
    llm_duration = llm_end - llm_start
    import json
    
    # Parse the JSON response to get the spoken text
    try:
        ai_data = json.loads(ai_text)
        spoken_text = ai_data.get("response_text", ai_text)
        print(f"Spoken Text: {spoken_text}")
    except json.JSONDecodeError:
        spoken_text = ai_text
        print("Failed to parse JSON, using raw text")

    print("\n--- MEASURING TTS (Audio Generation) ---")
    tts_start = time.time()
    await text_to_speech(spoken_text, "nova", "mp3")
    tts_end = time.time()
    tts_duration = tts_end - tts_start
    print(f"TTS Duration: {tts_duration:.4f}s")

    total_latency = stt_duration + llm_duration + tts_duration
    print(f"\n✅ Total Latency (LLM + TTS): {total_latency:.4f}s")

if __name__ == "__main__":
    asyncio.run(test_latency())
