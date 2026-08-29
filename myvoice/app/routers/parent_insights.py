"""Parent Insights API — keywords, sentiment, timeline, language mix, behavior patterns."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.core.security import get_current_family_id
from app.routers.parent_dashboard import verify_child_ownership
from app.services.insights_service import InsightsService

router = APIRouter(prefix="/insights", tags=["Parent - Insights"])


@router.get("/keywords")
async def get_keywords(
    child_id: UUID,
    days: int = Query(30, ge=7, le=90),
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    await verify_child_ownership(db, family_id, child_id)
    return await InsightsService.get_keywords(db, child_id, days)


@router.get("/sentiment")
async def get_sentiment(
    child_id: UUID,
    days: int = Query(30, ge=7, le=90),
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    await verify_child_ownership(db, family_id, child_id)
    return await InsightsService.get_sentiment_summary(db, child_id, days)


@router.get("/timeline")
async def get_timeline(
    child_id: UUID,
    days: int = Query(14, ge=7, le=30),
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    await verify_child_ownership(db, family_id, child_id)
    return await InsightsService.get_activity_timeline(db, child_id, days)


@router.get("/language-mix")
async def get_language_mix(
    child_id: UUID,
    days: int = Query(30, ge=7, le=90),
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    await verify_child_ownership(db, family_id, child_id)
    return await InsightsService.get_language_mix(db, child_id, days)


@router.get("/behavior")
async def get_behavior_patterns(
    child_id: UUID,
    days: int = Query(30, ge=7, le=90),
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    await verify_child_ownership(db, family_id, child_id)
    return await InsightsService.get_behavior_patterns(db, child_id, days)
