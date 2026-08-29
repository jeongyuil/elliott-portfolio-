from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.curriculum import Activity, CurriculumUnit
from app.models.session import Session as DbSession
from app.models.skill import TaskAttempt

class CurriculumEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_next_activity(self, child_id: str, story_theme: str | None = None) -> Activity | None:
        """
        Determines the next activity for a child based on their session history.
        If story_theme is provided, only considers activities from that story.
        """
        # 1. Get all activities sorted (by Week, then by ID/Order)
        all_activities = await self._get_all_activities_sorted(story_theme)
        if not all_activities:
            return None

        # 2. Find the last activity the child interacted with
        last_session_activity = await self._get_last_session_activity(child_id)

        if not last_session_activity:
            # No history -> Start from the very first activity
            return all_activities[0]

        # 3. Determine next step
        # Find index of last activity
        try:
            current_index = next(i for i, a in enumerate(all_activities) 
                               if a.activity_id == last_session_activity.activity_id)
        except StopIteration:
            # Last activity not found in current curriculum (maybe deprecated), start over or safe fallback
            return all_activities[0]

        # If the last activity was completed, move to the next one
        # If it was abandoned or failed, we might want to repeat it (or logic can be more complex)
        # For MVP: If 'completed', move next. Else, repeat.
        if last_session_activity.status == 'completed':
            next_index = current_index + 1
            if next_index < len(all_activities):
                return all_activities[next_index]
            else:
                # Curriculum finished! 
                # Could return a specific "All Done" activity or None
                return None
        else:
            # Retry the same activity
            return all_activities[current_index]

    async def _get_last_session_activity(self, child_id: str):
        # Join SessionActivity with Session to filter by child_id
        from app.models.session import SessionActivity
        
        stmt = (
            select(SessionActivity)
            .join(DbSession, SessionActivity.session_id == DbSession.session_id)
            .where(DbSession.child_id == child_id)
            .order_by(desc(SessionActivity.created_at if hasattr(SessionActivity, 'created_at') else DbSession.start_time)) 
            # SessionActivity doesn't have created_at, use Session.start_time or SessionActivity.started_at
            .limit(1)
        )
        # Note: SessionActivity table def in Step 2965 has started_at, ended_at. created_at is missing. 
        # But sorting by Session.start_time is safe.
        
        # Refined query:
        stmt = (
            select(SessionActivity)
            .join(DbSession, SessionActivity.session_id == DbSession.session_id)
            .where(DbSession.child_id == child_id)
            .order_by(desc(DbSession.start_time)) # Most recent session first
            .limit(1)
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()

    async def _get_all_activities_sorted(self, story_theme: str | None = None) -> list[Activity]:
        # Sort by CurriculumUnit week, then Activity ID (naive but functional for W1-A1 naming)
        stmt = (
            select(Activity)
            .join(CurriculumUnit, Activity.curriculum_unit_id == CurriculumUnit.curriculum_unit_id)
        )
        if story_theme:
            stmt = stmt.where(CurriculumUnit.story_theme == story_theme)
        stmt = stmt.order_by(CurriculumUnit.week, Activity.activity_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
