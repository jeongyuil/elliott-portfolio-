from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime, time

from app.database import get_db
from app.core.security import get_current_child_id
from app.models import SkillLevel
from app.schemas.skill import SkillLevelResponse, SkillListResponse

router = APIRouter()

@router.get("", response_model=SkillListResponse)
async def get_kid_skills(
    child_id: str = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the latest skill levels for the current child.
    """
    # For now, we get the latest snapshot per skill_id
    # A simple way is to get all snapshots for today, or order by date desc distinct on skill_id
    # But for MVP, let's just get all skill levels for the child, ordered by date desc
    
    stmt = select(SkillLevel).where(
        SkillLevel.child_id == UUID(child_id)
    ).order_by(SkillLevel.snapshot_date.desc())
    
    result = await db.execute(stmt)
    skills = result.scalars().all()
    
    # Filter to unique skill_id (latest)
    latest_skills_map = {}
    for s in skills:
        if s.skill_id not in latest_skills_map:
            latest_skills_map[s.skill_id] = s
            
    return SkillListResponse(items=list(latest_skills_map.values()))
