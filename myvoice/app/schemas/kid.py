from typing import List, Optional
from uuid import UUID

from app.schemas.base import CamelModel

class ChildStats(CamelModel):
    total_study_time: int
    missions_completed: int
    vocabulary_learned: int
    pronunciation_accuracy: float

class ChildProfileResponse(CamelModel):
    child_id: UUID
    name: str
    nickname: Optional[str] = None
    avatar_emoji: Optional[str] = None
    avatar_id: Optional[str] = None # Added for 3D Avatars
    avatar_url: Optional[str] = None # Helper for frontend
    level: int
    xp: int
    streak: int
    stats: ChildStats
    onboarding_completed: bool = False
    available_avatars: List[dict] = [] # List of {id, name, image}

class WeeklyGoalResponse(CamelModel):
    xp_current: int
    xp_target: int
    missions_current: int
    missions_target: int
    study_time_current: int
    study_time_target: int
    words_current: int
    words_target: int

class AdventureSummary(CamelModel):
    session_id: str
    title: str
    emoji: str
    status: str
    difficulty: str
    week: int = 1
    order: int = 0
    earned_stars: Optional[int] = None
    earned_xp: Optional[int] = None

class DailyBonusResponse(CamelModel):
    stars_reward: int
    consecutive_days: int
    new_stars: int
    new_streak: int

class KidHomeResponse(CamelModel):
    child: ChildProfileResponse
    weekly_goals: WeeklyGoalResponse
    recent_adventures: List[AdventureSummary]
    streak: int
    stars: int
    daily_bonus_available: bool

class AdventureCompleteRequest(CamelModel):
    stars: int
    xp: int

class StoryThemeResponse(CamelModel):
    theme: str
    title: str
    description: str
    emoji: str
    cover_color: str
    total_units: int = 0
    completed_units: int = 0

class StorySelectRequest(CamelModel):
    theme: str
