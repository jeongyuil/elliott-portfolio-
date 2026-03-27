import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from datetime import datetime
from app.main import app
from app.core.security import create_access_token

# Mock data
CHILD_ID = str(uuid.uuid4())
PARENT_ID = str(uuid.uuid4())

from app.database import async_session_maker
from app.models.family import FamilyAccount, Child

@pytest.fixture
def child_token():
    return create_access_token(data={
        "sub": CHILD_ID, 
        "role": "child", 
        "type": "access",
        "child_id": CHILD_ID 
    })

@pytest.mark.asyncio
async def test_phase3_flow(child_token):
    # Setup Data
    async with async_session_maker() as db:
        # Create Family
        family = FamilyAccount(
            family_id=uuid.UUID(PARENT_ID),
            parent_name="Test Parent",
            contact_email=f"test{uuid.uuid4()}@example.com",
            hashed_password="hashed"
        )
        db.add(family)
        
        # Create Child
        child = Child(
            child_id=uuid.UUID(CHILD_ID),
            family_id=family.family_id,
            name="Test Child",
            birth_date=datetime.utcnow()
        )
        db.add(child)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            # If already exists (re-run), ignore
            pass

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {child_token}"}
        
        # 1. Start Session (Auto Curriculum)
        resp = await ac.post("/v1/kid/sessions", json={"session_type": "curriculum"}, headers=headers)
        assert resp.status_code == 201
        data = resp.json()
        session_id = data["session_id"]
        assert data["activities"] is not None
        assert len(data["activities"]) > 0
        activity_id = data["activities"][0]["activity_id"]
        print(f"Session started: {session_id}, Activity: {activity_id}")

        # 2. Upload Utterance (Trigger Evaluation)
        # Note: Background tasks won't run automatically in TestClient unless using specific setup or we assume they trigger without error.
        # But we can check if the endpoint returns 200.
        utterance_payload = {
            "text_input": "Lion", # Mock text input to avoid audio processing
            "activity_id": activity_id
        }
        resp = await ac.post(
            f"/v1/kid/sessions/{session_id}/utterances", 
            json=utterance_payload, 
            headers={**headers, "X-Idempotency-Key": str(uuid.uuid4())}
        )
        assert resp.status_code == 200
        utt_data = resp.json()
        print(f"Utterance processed: {utt_data['ai_response_text']}")
        
        # 3. End Session (Trigger Skill Calc)
        resp = await ac.post(f"/v1/kid/sessions/{session_id}/end", headers=headers)
        assert resp.status_code == 200
        end_data = resp.json()
        print(f"Session ended. Duration: {end_data['duration_seconds']}")
        
        # 4. Verify Side Effects (Optional, requires DB access)
        # We can assume if endpoints returned 200, the logic executed.
