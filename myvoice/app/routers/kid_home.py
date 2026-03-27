from datetime import date, datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.core.security import get_current_child_id
from app.models import Child, WeeklyGoal, ChildInventory, Session, CurriculumUnit
from app.schemas.kid import KidHomeResponse, ChildProfileResponse, WeeklyGoalResponse, AdventureSummary, DailyBonusResponse
from app.schemas.kid import ChildStats

router = APIRouter()

# ---------------------------------------------------------------------------
# Star regeneration config
# ---------------------------------------------------------------------------
STAR_REGEN_PER_HOUR = 5
STAR_REGEN_MAX_PENDING = 50   # Max stars that can accumulate while away
STAR_MAX_BALANCE = 500        # Soft cap — regen stops here


def apply_star_regen(inventory: ChildInventory) -> int:
    """Apply passive star regeneration based on elapsed time. Returns stars granted."""
    now = datetime.now(timezone.utc)
    if not inventory.last_star_regen_at:
        inventory.last_star_regen_at = now
        return 0

    elapsed = now - inventory.last_star_regen_at
    hours = elapsed.total_seconds() / 3600

    if hours < 1 or inventory.stars >= STAR_MAX_BALANCE:
        return 0

    regen = min(int(hours) * STAR_REGEN_PER_HOUR, STAR_REGEN_MAX_PENDING)
    regen = min(regen, STAR_MAX_BALANCE - inventory.stars)

    if regen > 0:
        inventory.stars += regen
        inventory.last_star_regen_at = now

    return regen

@router.get("", response_model=KidHomeResponse)
async def get_kid_home(
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    # 1. Get Child & Inventory
    stmt = select(Child).where(Child.child_id == child_id)
    result = await db.execute(stmt)
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    # Ensure inventory exists
    if not child.inventory:
        inventory = ChildInventory(child_id=child_id)
        db.add(inventory)
        child.inventory = inventory
        await db.commit()

    # Apply passive star regeneration
    regen = apply_star_regen(child.inventory)
    if regen > 0:
        await db.commit()

    # 2. Get/Create Weekly Goal
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

    # 3. Get today's recommended adventures (first 3 curriculum units)
    unit_stmt = select(CurriculumUnit).order_by(CurriculumUnit.week).limit(3)
    unit_result = await db.execute(unit_stmt)
    units = unit_result.scalars().all()

    recent_adventures = []
    for i, unit in enumerate(units):
        status = "unlocked" if unit.week == 1 else "locked"
        recent_adventures.append(AdventureSummary(
            session_id=unit.curriculum_unit_id,
            title=unit.title,
            emoji="🚀",
            status=status,
            difficulty="보통",
            earned_stars=None,
            earned_xp=None
        ))
    
    # 4. Calculate stats (simplified)
    # In real app, we would aggregate Session data
    child_stats = ChildStats(
        total_study_time=0,
        missions_completed=0,
        vocabulary_learned=0, # Aggregate from VocabularyProgress
        pronunciation_accuracy=0.0
    )

    child_profile = ChildProfileResponse(
        child_id=child.child_id,
        name=child.name,
        nickname=child.nickname,
        avatar_emoji=child.avatar_emoji,
        level=child.level,
        xp=child.xp,
        streak=child.inventory.streak,
        stats=child_stats,
        onboarding_completed=child.onboarding_completed
    )

    return KidHomeResponse(
        child=child_profile,
        weekly_goals=WeeklyGoalResponse.model_validate(goal),
        recent_adventures=recent_adventures,
        streak=child.inventory.streak,
        stars=child.inventory.stars,
        daily_bonus_available=child.inventory.last_active_date < today if child.inventory.last_active_date else True
    )

@router.post("/daily-bonus", response_model=DailyBonusResponse)
async def claim_daily_bonus(
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(ChildInventory).where(ChildInventory.child_id == child_id)
    result = await db.execute(stmt)
    inventory = result.scalar_one_or_none()
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
        
    today = date.today()
    if inventory.last_active_date == today:
        raise HTTPException(status_code=400, detail="Already claimed daily bonus")
        
    # Logic: streak + 1 if yesterday, else 1
    if inventory.last_active_date == today - timedelta(days=1):
        inventory.streak += 1
    else:
        inventory.streak = 1
        
    # Streak-scaled rewards: base 50 + 10 per streak day (max 100)
    stars_reward = min(50 + (inventory.streak * 10), 100)

    inventory.stars += stars_reward
    inventory.last_active_date = today

    await db.commit()

    return DailyBonusResponse(
        stars_reward=stars_reward,
        consecutive_days=inventory.streak,
        new_stars=inventory.stars,
        new_streak=inventory.streak
    )
