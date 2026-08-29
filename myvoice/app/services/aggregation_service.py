from datetime import date, timedelta, datetime
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models import ChildInventory, Session, Child

class AggregationService:
    @staticmethod
    async def update_daily_activity(db: AsyncSession, child_id: UUID) -> dict:
        """
        Update streak and daily activity stats.
        Should be called when a session is completed.
        """
        # 1. Get or Create Inventory
        stmt = select(ChildInventory).where(ChildInventory.child_id == child_id)
        result = await db.execute(stmt)
        inventory = result.scalar_one_or_none()
        
        if not inventory:
            inventory = ChildInventory(child_id=child_id, streak=0, last_active_date=None)
            db.add(inventory)
            await db.flush() # To get ID if needed, but we have object ref

        today = date.today()
        last_active = inventory.last_active_date
        
        streak_updated = False
        
        # 2. Update Streak
        if last_active != today:
            if last_active == today - timedelta(days=1):
                # Consecutive day
                inventory.streak += 1
            elif last_active is None or last_active < today - timedelta(days=1):
                # Broken streak or first time
                inventory.streak = 1
            # If last_active > today (future?), ignore or handle error. Assuming correct time.
            
            inventory.last_active_date = today
            streak_updated = True
            await db.commit()
            await db.refresh(inventory)
            
        return {
            "streak": inventory.streak,
            "streak_updated": streak_updated
        }

    @staticmethod
    async def get_weekly_stats(db: AsyncSession, child_id: UUID) -> dict:
        """
        Get aggregated stats for the current week (Mon-Sun or last 7 days).
        Returns: {
            "total_sessions": int,
            "total_learning_time_minutes": int,
            "daily_breakdown": [{"day": "Mon", "minutes": 10}, ...]
        }
        """
        # Define "Week" as last 7 days including today
        today = date.today()
        start_date = today - timedelta(days=6)
        
        # Query Sessions
        stmt = select(Session).where(
            Session.child_id == child_id,
            Session.start_time >= datetime.combine(start_date, datetime.min.time())
        )
        result = await db.execute(stmt)
        sessions = result.scalars().all()
        
        total_sessions = len(sessions)
        total_seconds = sum(s.duration_seconds for s in sessions if s.duration_seconds)
        total_minutes = total_seconds // 60
        
        # Daily Breakdown
        daily_map = { (start_date + timedelta(days=i)): 0 for i in range(7) }
        
        for s in sessions:
            s_date = s.start_time.date()
            if s_date in daily_map:
                daily_map[s_date] += (s.duration_seconds or 0) // 60
                
        daily_breakdown = []
        days_str = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] # Or localized
        # Actually better to return date string or day name
        for d in sorted(daily_map.keys()):
            daily_breakdown.append({
                "date": d.isoformat(),
                "day_name": d.strftime("%a"), # Mon, Tue...
                "minutes": daily_map[d]
            })
            
        return {
            "total_sessions": total_sessions,
            "total_learning_time_minutes": total_minutes,
            "daily_breakdown": daily_breakdown
        }
