import logging
import math
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Child

logger = logging.getLogger(__name__)

# Constants
XP_PER_LEVEL = 100
XP_PER_MINUTE = 10
XP_PER_TURN = 5
XP_BONUS_COMPLETION = 50

class GamificationService:
    @staticmethod
    def calculate_level(total_xp: int) -> int:
        """
        Calculate level based on total XP.
        Formula: Level = 1 + floor(Total XP / 100)
        """
        return 1 + (total_xp // XP_PER_LEVEL)

    @staticmethod
    def get_level_progress(total_xp: int):
        """
        Get progress towards next level.
        Returns (current_level_xp, next_level_xp, percentage)
        """
        current_level = GamificationService.calculate_level(total_xp)
        current_level_xp = total_xp % XP_PER_LEVEL
        next_level_xp = XP_PER_LEVEL
        percentage = min(100, int((current_level_xp / next_level_xp) * 100))
        
        return {
            "level": current_level,
            "current_xp": current_level_xp,
            "next_level_xp": next_level_xp,
            "percentage": percentage
        }

    @staticmethod
    async def award_xp(db: AsyncSession, child_id: str, amount: int, source: str) -> dict:
        """
        Award XP to a child and handle level up.
        Returns dict with earned details and level up status.
        """
        # 1. Get Child
        from uuid import UUID
        stmt = select(Child).where(Child.child_id == UUID(child_id))
        result = await db.execute(stmt)
        child = result.scalar_one_or_none()
        
        if not child:
            logger.error(f"Child {child_id} not found for awarding XP")
            return {"earned_xp": 0, "level_up": False, "new_level": 1}

        # 2. Update XP
        old_level = child.level
        child.xp += amount
        
        # 3. Check Level Up
        new_level = GamificationService.calculate_level(child.xp)
        level_up = new_level > old_level
        
        if level_up:
            child.level = new_level
            logger.info(f"Child {child_id} leveled up to {new_level}!")
            
        await db.commit()
        await db.refresh(child)
        
        return {
            "earned_xp": amount,
            "total_xp": child.xp,
            "level": child.level,
            "level_up": level_up,
            "previous_level": old_level
        }

    @staticmethod
    def calculate_session_xp(duration_seconds: int, turns: int, is_completed: bool = True) -> int:
        """
        Calculate XP earned from a session.
        """
        minutes = math.ceil(duration_seconds / 60)
        xp = (minutes * XP_PER_MINUTE) + (turns * XP_PER_TURN)
        
        if is_completed:
            xp += XP_BONUS_COMPLETION
            
        return xp
