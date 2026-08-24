"""Sessions router: start, utterance, end."""
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.session import Session
from app.models.utterance import Utterance
from app.schemas.session import (
    SessionCreate, SessionResponse,
    SessionEndResponse,
    UtteranceRequest, UtteranceResponse,
)
from app.core.security import get_current_family_id

router = APIRouter()


@router.post("", response_model=SessionResponse, status_code=201)
async def start_session(
    req: SessionCreate,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    session = Session(
        child_id=req.child_id,
        session_type=req.session_type,
        status="active",
    )
    db.add(session)
    await db.flush()
    return session


@router.post("/{session_id}/utterances", response_model=UtteranceResponse)
async def upload_utterance(
    session_id: uuid.UUID,
    req: UtteranceRequest,
    x_idempotency_key: str = Header(..., alias="X-Idempotency-Key"),
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    # Verify session exists and is active
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Session is not active")

    # TODO: Idempotency check via Redis
    # TODO: STT → LLM → TTS pipeline (Phase 2)

    utterance = Utterance(
        session_id=session_id,
        turn_index=req.chunk_index or 0,
        speaker_type="child",
        text_raw="[STT pending]",
    )
    db.add(utterance)
    await db.flush()

    return UtteranceResponse(
        utterance_id=utterance.utterance_id,
        text_transcript="[STT pipeline not yet connected]",
        speaker_type="child",
    )


@router.post("/{session_id}/end", response_model=SessionEndResponse)
async def end_session(
    session_id: uuid.UUID,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.status = "ended"
    session.end_time = datetime.utcnow()
    if session.start_time:
        session.duration_seconds = int((session.end_time - session.start_time).total_seconds())

    return SessionEndResponse(
        duration_seconds=session.duration_seconds or 0,
        engagement_score=session.engagement_score,
    )
