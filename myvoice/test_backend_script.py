import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

async def test_flow():
    print("Testing Backend Flow (Real Server)...")
    
    # Use real server
    async with AsyncClient(base_url="http://localhost:8000") as client:
        # 1. Login Parent Mock
        print("1. Login Parent Mock")
        r = await client.post("/v1/auth/login/mock", json={"role": "parent"})
        if r.status_code != 200:
            print(f"Login Failed: {r.status_code} {r.text}")
            return
        tokens = r.json()
        access_token = tokens["access_token"]
        print(f"Access Token: {access_token[:20]}...")
        
        # 2. Get Children
        print("2. Get Children")
        headers = {"Authorization": f"Bearer {access_token}"}
        r = await client.get("/v1/parent/children", headers=headers)
        if r.status_code != 200:
            print(f"Get Children Failed: {r.status_code} {r.text}")
            # If 401, token is bad.
            return
        children = r.json()
        if not children:
            print("No children found.")
            return
        child_id = children[0]["child_id"]
        print(f"Child ID: {child_id}")
        
        # 3. Select Child (Get Child Token)
        print("3. Select Child")
        r = await client.post("/v1/auth/select-child", headers=headers, json={"child_id": child_id})
        if r.status_code != 200:
            print(f"Select Child Failed: {r.status_code} {r.text}")
            return
        child_token_data = r.json()
        child_token = child_token_data["child_token"] # Response key is child_token
        child_headers = {"Authorization": f"Bearer {child_token}"}
        print(f"Child Token: {child_token[:20]}...")
        
        # 4. Get Adventures
        print("4. Get Adventures")
        r = await client.get("/v1/kid/adventures", headers=child_headers)
        if r.status_code != 200:
            print(f"Get Adventures Failed: {r.status_code} {r.text}")
            # Continue anyway
            
        adventures = r.json()
        if not adventures:
            print("No adventures returned.")
            return

        adventure_id = adventures[0]["sessionId"]
        print(f"Adventure ID: {adventure_id}")
        
        # 5. Start Session
        print("5. Start Session")
        payload = {
            "child_id": child_id,
            "session_type": "curriculum",
            "curriculum_unit_id": adventure_id
        }
        r = await client.post("/v1/kid/sessions", headers=child_headers, json=payload)
        
        if r.status_code not in (200, 201):
            print(f"Start Session Failed: {r.status_code} {r.text}")
            return
            
        session_data = r.json()
        session_id = session_data["session_id"]
        print(f"Session Started: {session_id}")
        
        # 6. Generate TTS (Narrator) - Backend TTS might fail, but let's see.
        print("6. Generate TTS")
        tts_payload = {"text": "Hello World", "voice": "alloy"}
        r = await client.post(f"/v1/kid/sessions/{session_id}/tts", headers=child_headers, json=tts_payload)
        if r.status_code != 200:
            print(f"TTS Failed (Expected if quota exceeded): {r.status_code} {r.text}")
        else:
            print("TTS Success")
            
        # 7. Upload Utterance (Text Input)
        print("7. Upload Utterance (Text Input)")
        # Send "dog" to trigger Mock AI positive response
        utterance_payload = {
            "text_input": "Run dog run",
            "activity_id": None # Optional
        }
        r = await client.post(
            f"/v1/kid/sessions/{session_id}/utterances", 
            headers={**child_headers, "X-Idempotency-Key": "test-idempotency-key"}, 
            json=utterance_payload
        )
        if r.status_code != 200:
             print(f"Utterance Failed: {r.status_code} {r.text}")
             return
             
        utt_resp = r.json()
        print("Utterance Response:")
        print(f"Child: {utt_resp['child_text']}")
        print(f"AI: {utt_resp['ai_response_text']}")
        print(f"Audio Base64: {utt_resp['ai_response_audio_base64'][:20]}...")
        if utt_resp['feedback']:
            print(f"Feedback: {utt_resp['feedback']}")

if __name__ == "__main__":
    try:
        asyncio.run(test_flow())
    except Exception as e:
        print(f"Test Exception: {e}")
        import traceback
        traceback.print_exc()
