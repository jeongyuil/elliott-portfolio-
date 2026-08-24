"""Trial router: quick-start without login (FDD 4.0)."""
import uuid
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class QuickStartRequest(BaseModel):
    device_id: str


class QuickStartResponse(BaseModel):
    temp_session_id: uuid.UUID
    token: str


@router.post("/quick-start", response_model=QuickStartResponse, status_code=201)
async def quick_start(req: QuickStartRequest):
    """
    One-Handed Onboarding: 계정 없이 즉시 체험 세션 시작.
    Flow: [앱 설치] → [Quick Trial] → [아이의 반응 확인] → [계정 생성]
    """
    # TODO: Create ephemeral session & temporary token
    temp_session_id = uuid.uuid4()
    temp_token = f"temp_{uuid.uuid4().hex[:16]}"
    return QuickStartResponse(temp_session_id=temp_session_id, token=temp_token)
