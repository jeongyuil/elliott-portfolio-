from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.core.security import get_current_child_id
from app.models import Child, Session, VocabularyProgress, ChildInventory
from app.schemas.kid import ChildProfileResponse, ChildStats

router = APIRouter()

@router.get("", response_model=ChildProfileResponse)
async def get_kid_profile(
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    # 1. Get Child
    stmt = select(Child).where(Child.child_id == child_id)
    result = await db.execute(stmt)
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
        
    # 2. Get Stats
    # Vocabulary
    vocab_stmt = select(func.sum(VocabularyProgress.words_learned)).where(VocabularyProgress.child_id == child_id)
    vocab_result = await db.execute(vocab_stmt)
    total_words = vocab_result.scalar() or 0
    
    # Sessions
    session_stmt = select(func.count(Session.session_id)).where(Session.child_id == child_id, Session.status == "ended")
    session_result = await db.execute(session_stmt)
    total_missions = session_result.scalar() or 0
    
    time_stmt = select(func.sum(Session.duration_seconds)).where(Session.child_id == child_id)
    time_result = await db.execute(time_stmt)
    total_seconds = time_result.scalar() or 0
    total_minutes = total_seconds // 60
    
    # Pronunciation (Mock logic for now as we don't store individual task attempts permanently in this phase)
    # In Phase 4 we will query TaskAttempt table
    accuracy = 85.0 # Placeholder
    
    stats = ChildStats(
        total_study_time=total_minutes,
        missions_completed=total_missions,
        vocabulary_learned=total_words,
        pronunciation_accuracy=accuracy
    )
    
    # Ensure inventory for streak
    if not child.inventory:
        child.inventory = ChildInventory(child_id=child_id)
        db.add(child.inventory)
        await db.commit()
    
    
    # Available Avatars (High Quality Assets)
    available_avatars = [
        {"id": "avatar_rabbit_3d", "name": "토끼", "image": "/assets/avatars/avatar_rabbit_3d.png"},
        {"id": "avatar_tiger_3d", "name": "호랑이", "image": "/assets/avatars/avatar_tiger_3d.png"},
        {"id": "avatar_bear_3d", "name": "곰", "image": "/assets/avatars/avatar_bear_3d.png"},
        {"id": "avatar_fox_3d", "name": "여우", "image": "/assets/avatars/avatar_fox_3d.png"},
        {"id": "avatar_robot_3d", "name": "로봇", "image": "/assets/avatars/avatar_robot_3d.png"},
        {"id": "avatar_unicorn_3d", "name": "유니콘", "image": "/assets/avatars/avatar_unicorn_3d.png"},
    ]
    
    # Determine avatar URL
    avatar_url = None
    if child.avatar_id and "avatar_" in child.avatar_id:
        avatar_url = f"/assets/avatars/{child.avatar_id}.png"
    elif child.avatar_emoji:
        # Legacy fallback if needed, or maybe just ignore
        pass

    return ChildProfileResponse(
        child_id=child.child_id,
        name=child.name,
        nickname=child.nickname,
        avatar_emoji=child.avatar_emoji,
        avatar_id=child.avatar_id,
        avatar_url=avatar_url,
        level=child.level,
        xp=child.xp,
        streak=child.inventory.streak,
        stats=stats,
        onboarding_completed=child.onboarding_completed,
        available_avatars=available_avatars
    )

from pydantic import BaseModel
class AvatarUpdateRequest(BaseModel):
    avatar_id: str

@router.patch("/avatar")
async def update_avatar(
    req: AvatarUpdateRequest,
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Child).where(Child.child_id == child_id)
    result = await db.execute(stmt)
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
        
    # Validation: Ensure avatar_id is in our list (or at least valid format)
    child.avatar_id = req.avatar_id 
    
    await db.commit()
    return {"status": "success", "avatar_id": req.avatar_id}
