"""
E2E Test: Voice Session Flow
start session → send utterances → end session → verify XP/gamification
"""
import uuid


class TestVoiceSessionFlow:
    """Full voice session lifecycle with mocked OpenAI."""

    async def test_start_session(self, client, child_token, seed_family):
        """POST /v1/kid/sessions → 201 with session_id."""
        resp = await client.post("/v1/kid/sessions", json={
            "session_type": "curriculum",
        }, headers={"Authorization": f"Bearer {child_token}"})
        assert resp.status_code == 201
        data = resp.json()
        assert "session_id" in data
        assert data["status"] == "active"
        assert data["child_id"] == seed_family["child_id"]

    async def test_full_session_flow(self, client, child_token):
        """Start → utterance (text) → utterance (text) → end."""
        headers = {"Authorization": f"Bearer {child_token}"}

        # 1. Start session
        resp = await client.post("/v1/kid/sessions", json={
            "session_type": "curriculum",
        }, headers=headers)
        assert resp.status_code == 201
        session_id = resp.json()["session_id"]

        # 2. First utterance (text input, bypassing STT)
        resp = await client.post(
            f"/v1/kid/sessions/{session_id}/utterances",
            json={"text_input": "Go! Let's start!"},
            headers={**headers, "X-Idempotency-Key": str(uuid.uuid4())},
        )
        assert resp.status_code == 200
        utt1 = resp.json()
        assert utt1["child_text"] == "Go! Let's start!"
        assert utt1["ai_response_text"]  # AI responded
        assert utt1["speaker_type"] == "ai"

        # 3. Second utterance
        resp = await client.post(
            f"/v1/kid/sessions/{session_id}/utterances",
            json={"text_input": "I see a big lion!"},
            headers={**headers, "X-Idempotency-Key": str(uuid.uuid4())},
        )
        assert resp.status_code == 200
        utt2 = resp.json()
        assert utt2["ai_response_text"]

        # 4. End session
        resp = await client.post(
            f"/v1/kid/sessions/{session_id}/end",
            headers=headers,
        )
        assert resp.status_code == 200
        end_data = resp.json()
        assert end_data["duration_seconds"] >= 0
        assert end_data["total_turns"] >= 2  # At least child + AI utterances
        assert end_data["earned_xp"] >= 0

    async def test_idempotency(self, client, child_token):
        """Same idempotency key → returns cached response."""
        headers = {"Authorization": f"Bearer {child_token}"}

        resp = await client.post("/v1/kid/sessions", json={
            "session_type": "curriculum",
        }, headers=headers)
        session_id = resp.json()["session_id"]

        idem_key = str(uuid.uuid4())

        # First request
        resp1 = await client.post(
            f"/v1/kid/sessions/{session_id}/utterances",
            json={"text_input": "Hello!"},
            headers={**headers, "X-Idempotency-Key": idem_key},
        )
        assert resp1.status_code == 200

        # Same idempotency key → should return cached
        resp2 = await client.post(
            f"/v1/kid/sessions/{session_id}/utterances",
            json={"text_input": "Hello!"},
            headers={**headers, "X-Idempotency-Key": idem_key},
        )
        assert resp2.status_code == 200
        assert resp2.json()["utterance_id"] == resp1.json()["utterance_id"]

    async def test_utterance_no_auth(self, client):
        """Utterance without auth → 401."""
        resp = await client.post(
            f"/v1/kid/sessions/{uuid.uuid4()}/utterances",
            json={"text_input": "Hello!"},
            headers={"X-Idempotency-Key": str(uuid.uuid4())},
        )
        assert resp.status_code == 401

    async def test_utterance_invalid_session(self, client, child_token):
        """Utterance on non-existent session → 404."""
        resp = await client.post(
            f"/v1/kid/sessions/{uuid.uuid4()}/utterances",
            json={"text_input": "Hello!"},
            headers={
                "Authorization": f"Bearer {child_token}",
                "X-Idempotency-Key": str(uuid.uuid4()),
            },
        )
        assert resp.status_code == 404

    async def test_end_nonexistent_session(self, client, child_token):
        """End non-existent session → 404."""
        resp = await client.post(
            f"/v1/kid/sessions/{uuid.uuid4()}/end",
            headers={"Authorization": f"Bearer {child_token}"},
        )
        assert resp.status_code == 404

    async def test_tts_endpoint(self, client, child_token):
        """POST /v1/kid/sessions/{id}/tts → audio_base64."""
        headers = {"Authorization": f"Bearer {child_token}"}

        # Start a session first
        resp = await client.post("/v1/kid/sessions", json={
            "session_type": "curriculum",
        }, headers=headers)
        session_id = resp.json()["session_id"]

        # TTS
        resp = await client.post(
            f"/v1/kid/sessions/{session_id}/tts",
            json={"text": "Hello, friend!", "character": "luna"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert "audio_base64" in resp.json()
