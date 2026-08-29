from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.core.security import get_current_child_id
from app.models import WeeklyGoal
from app.schemas.kid import WeeklyGoalResponse

router = APIRouter()

@router.get("", response_model=WeeklyGoalResponse)
async def get_weekly_goals(
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    
    stmt = select(WeeklyGoal).where(
        and_(WeeklyGoal.child_id == child_id, WeeklyGoal.week_start == week_start)
    )
    result = await db.execute(stmt)
    goal = result.scalar_one_or_none()
    
    if not goal:
        goal = WeeklyGoal(child_id=child_id, week_start=week_start)
        db.add(goal)
        await db.commit()
        await db.refresh(goal)
        
    return WeeklyGoalResponse.model_validate(goal)

@router.post("", response_model=WeeklyGoalResponse)
async def update_weekly_goals(
    targets: dict, # Simplified: Accept partial updates
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    
    stmt = select(WeeklyGoal).where(
        and_(WeeklyGoal.child_id == child_id, WeeklyGoal.week_start == week_start)
    )
    result = await db.execute(stmt)
    goal = result.scalar_one_or_none()
    
    if not goal:
        goal = WeeklyGoal(child_id=child_id, week_start=week_start)
        db.add(goal)
    
    if "xp_target" in targets:
        goal.xp_target = targets["xp_target"]
    if "missions_target" in targets:
        goal.missions_target = targets["missions_target"]
    if "study_time_target" in targets:
        goal.study_time_target = targets["study_time_target"]
    if "words_target" in targets:
        goal.words_target = targets["words_target"]
        
    await db.commit()
    await db.refresh(goal)
    
    return WeeklyGoalResponse.model_validate(goal)
