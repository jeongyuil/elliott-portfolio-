import asyncio
import time
import os
import sys
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.safety_filter import filter_input
from app.services.openai_service import chat_with_ai, text_to_speech
from app.services.conversation_manager import build_system_prompt

async def verify_pipeline():
    print("🧪 Starting Speech Pipeline Verification...")
    
    # ---------------------------------------------------------
    # 1. Safety Filter Verification
    # ---------------------------------------------------------
    print("\n[1/3] Verifying Safety Filter...")
    unsafe_text = "You are a bad bitch"
    safety_result = filter_input(unsafe_text)
    
    if not safety_result.is_safe and safety_result.reason == "profanity_detected":
        print(f"✅ Safety Check Passed: Blocked '{unsafe_text}'")
        print(f"   Response: {safety_result.safe_text}")
    else:
        print(f"❌ Safety Check Failed: Did not block '{unsafe_text}'")
        return

    # ---------------------------------------------------------
    # 2. LLM Latency & Optimization Verification
    # ---------------------------------------------------------
    print("\n[2/3] Verifying LLM Optimization (Prompt Tuning)...")
    safe_text = "Hello! My name is Yuil. I like robots."
    
    # Check safety first (simulating real flow)
    if not filter_input(safe_text).is_safe:
        print("❌ Unexpected safety block for safe text.")
        return

    system_prompt = build_system_prompt(None, None)
    
    start_time = time.time()
    ai_response_json = await chat_with_ai(system_prompt, [], safe_text)
    llm_duration = time.time() - start_time
    
    try:
        response_data = json.loads(ai_response_json)
        spoken_text = response_data.get("response_text", "")
        feedback = response_data.get("feedback", {})
        
        print(f"✅ LLM Response Received in {llm_duration:.2f}s")
        print(f"   Text: {spoken_text}")
        print(f"   Feedback: {feedback.get('message', 'No feedback')}")
        
        # Verify brevity (heuristic: text length should be short)
        if len(spoken_text) > 150:
            print("⚠️ Warning: Response seems long for 'concise' instruction.")
        else:
            print("✅ Response Conciseness: OK")
            
    except json.JSONDecodeError:
        print(f"❌ LLM Failed to return JSON: {ai_response_json}")
        return

    # ---------------------------------------------------------
    # 3. TTS Latency Verification
    # ---------------------------------------------------------
    print("\n[3/3] Verifying TTS Latency...")
    start_time = time.time()
    audio_bytes = await text_to_speech(spoken_text, "nova")
    tts_duration = time.time() - start_time
    
    if len(audio_bytes) > 0:
        print(f"✅ TTS Generated {len(audio_bytes)} bytes in {tts_duration:.2f}s")
    else:
        print("❌ TTS Failed: Empty audio bytes")
        return
        
    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------
    total_latency = llm_duration + tts_duration
    print(f"\n✨ Verification Complete! Total Interaction Latency: {total_latency:.2f}s")

if __name__ == "__main__":
    asyncio.run(verify_pipeline())
