import pytest
from playwright.sync_api import Playwright, APIRequestContext, expect

import os
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8008")

@pytest.fixture(scope="module")
def api_context(playwright: Playwright) -> APIRequestContext:
    headers = {
        "Content-Type": "application/json",
    }
    request_context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers=headers,
    )
    yield request_context
    request_context.dispose()

def test_voice_session_flow(api_context: APIRequestContext):
    print(f"Testing against {BASE_URL}")
    
    # 1. Login (Parent)
    print("Step 1: Parent Login")
    login_res = api_context.post(f"/v1/auth/login/mock", data={})
    assert login_res.ok, f"Login failed: {login_res.status} {login_res.text()}"
    
    # 2. Get Children to find child_id
    print("Step 2: Get Children")
    children_res = api_context.get(f"/v1/parent/children")
    assert children_res.ok, f"Get children failed: {children_res.status} {children_res.text()}"
    children = children_res.json()
    assert len(children) > 0, "No children found"
    child_id = children[0]["child_id"]
    print(f"Found child: {child_id}")
    
    # 3. Select Child (Login as Kid)
    print("Step 3: Select Child")
    select_res = api_context.post(f"/v1/auth/select-child", data={"child_id": child_id})
    assert select_res.ok, f"Select child failed: {select_res.status} {select_res.text()}"
    
    # 4. Start Session
    print("Step 4: Start Session")
    start_res = api_context.post(f"/v1/kid/sessions", data={"session_type": "adventure"})
    assert start_res.ok, f"Start session failed: {start_res.status} {start_res.text()}"
    session_data = start_res.json()
    session_id = session_data["session_id"]
    assert session_id
    print(f"Session started: {session_id}")
    
    # 5. Send Utterance (Text Input)
    print("Step 5: Send Utterance 'Hello Luna'")
    # Using text_input to avoid mic setup, simpler for E2E
    utterance_res = api_context.post(
        f"/v1/kid/sessions/{session_id}/utterances", 
        data={
            "text_input": "Hello Luna, let's go!",
        },
        headers={"X-Idempotency-Key": "test-e2e-1"}
    )
    assert utterance_res.ok, f"Utterance failed: {utterance_res.status} {utterance_res.text()}"
    utterance_data = utterance_res.json()
    
    # 6. Verify Response
    print("Step 6: Verify Response")
    print(f"AI Text: {utterance_data.get('ai_response_text')}")
    assert utterance_data["child_text"] == "Hello Luna, let's go!"
    assert utterance_data["ai_response_text"], "No AI response text"
    # Audio might be None if TTS fails (mock logic?) but standard pipeline should return it.
    # If using OpenAI, it should work. If mock fallback, maybe not.
    # In safety test we saw empty response if filtered.
    # Here input is safe.
    assert utterance_data["speaker_type"] == "ai"
    
    # Optional: End Session
    print("Step 7: End Session")
    end_res = api_context.post(f"/v1/kid/sessions/{session_id}/end")
    assert end_res.ok
    print("Test Complete")
