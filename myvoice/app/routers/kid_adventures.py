import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.core.security import get_current_child_id
from app.models import CurriculumUnit, Session, ChildInventory, WeeklyGoal, Child, Activity
from app.schemas.kid import AdventureSummary, AdventureCompleteRequest, StoryThemeResponse, StorySelectRequest

logger = logging.getLogger("app.routers.kid_adventures")

SKIP_COST_STARS = 30

# Story theme metadata (static catalog)
STORY_CATALOG = {
    "earth_crew": {
        "title": "어스 크루 대모험",
        "description": "우주에서 온 루나의 지구 적응을 도와주세요! 인사, 감정, 옷 입기까지 — 루나의 지구 친구가 되어주는 이야기.",
        "emoji": "🚀",
        "cover_color": "from-indigo-500 to-purple-500",
    },
    "kpop_hunters": {
        "title": "케이팝 데몬 헌터스",
        "description": "음악의 별 멜로디아를 지켜라! 수습 아이돌 루나와 전설의 프로듀서 포포와 함께 노이즈 데몬을 물리치는 이야기.",
        "emoji": "🎤",
        "cover_color": "from-pink-500 to-rose-500",
    },
    "dino_expedition": {
        "title": "공룡 탐험대",
        "description": "시간 여행 포털을 통해 공룡 시대로! 아기 공룡 Trixie와 함께 화석을 발굴하고, 공룡 친구를 사귀는 대모험.",
        "emoji": "🦕",
        "cover_color": "from-emerald-500 to-teal-500",
    },
}

router = APIRouter()


@router.get("/stories", response_model=list[StoryThemeResponse])
async def get_stories(
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db),
):
    """Return available story themes with progress info."""
    from sqlalchemy import func

    # Get completed unit counts per theme
    session_stmt = select(Session).where(
        and_(Session.child_id == child_id, Session.curriculum_unit_id.isnot(None), Session.status == "ended")
    )
    session_result = await db.execute(session_stmt)
    ended_sessions = session_result.scalars().all()
    completed_unit_ids = {s.curriculum_unit_id for s in ended_sessions}

    # Count total units per theme
    units_stmt = select(CurriculumUnit.story_theme, func.count()).group_by(CurriculumUnit.story_theme)
    units_result = await db.execute(units_stmt)
    total_per_theme = dict(units_result.all())

    # Count completed units per theme
    all_units_stmt = select(CurriculumUnit)
    all_units = (await db.execute(all_units_stmt)).scalars().all()
    completed_per_theme: dict[str, int] = {}
    for u in all_units:
        if u.curriculum_unit_id in completed_unit_ids:
            completed_per_theme[u.story_theme] = completed_per_theme.get(u.story_theme, 0) + 1

    stories = []
    for theme, meta in STORY_CATALOG.items():
        stories.append(StoryThemeResponse(
            theme=theme,
            title=meta["title"],
            description=meta["description"],
            emoji=meta["emoji"],
            cover_color=meta["cover_color"],
            total_units=total_per_theme.get(theme, 0),
            completed_units=completed_per_theme.get(theme, 0),
        ))
    return stories


@router.post("/stories/select")
async def select_story(
    req: StorySelectRequest,
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db),
):
    """Set the child's active story theme."""
    if req.theme not in STORY_CATALOG:
        raise HTTPException(status_code=400, detail=f"Unknown story theme: {req.theme}")

    child = (await db.execute(select(Child).where(Child.child_id == child_id))).scalar_one()
    child.selected_story_theme = req.theme
    await db.commit()

    return {"status": "ok", "selected_story_theme": req.theme}


@router.get("", response_model=list[AdventureSummary])
async def get_adventures(
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    # 0. Get child's selected story theme
    child = (await db.execute(select(Child).where(Child.child_id == child_id))).scalar_one()
    story_theme = child.selected_story_theme
    if not story_theme:
        return []  # No story selected yet — frontend shows StorySelect

    # 1. Get curriculum units for this story theme
    stmt = (
        select(CurriculumUnit)
        .where(CurriculumUnit.story_theme == story_theme)
        .order_by(CurriculumUnit.week, CurriculumUnit.curriculum_unit_id)
    )
    result = await db.execute(stmt)
    units = result.scalars().all()

    # 2. Get completed sessions for this child
    # Treat both "ended" sessions AND "active" sessions with utterances as completed
    # (handles cases where user left without properly ending)
    from app.models import Utterance
    from sqlalchemy import func

    session_stmt = select(Session).where(
        and_(Session.child_id == child_id, Session.curriculum_unit_id.isnot(None))
    )
    session_result = await db.execute(session_stmt)
    sessions = session_result.scalars().all()

    # A unit is completed if it has an "ended" session
    # OR an "active" session with at least 2 utterances (real interaction happened)
    completed_unit_ids: set[str] = set()
    active_session_ids = []
    for s in sessions:
        if not s.curriculum_unit_id:
            continue
        if s.status == "ended":
            completed_unit_ids.add(s.curriculum_unit_id)
        elif s.status == "active":
            active_session_ids.append((s.session_id, s.curriculum_unit_id))

    # Check utterance counts for active sessions
    if active_session_ids:
        for sid, unit_id in active_session_ids:
            if unit_id in completed_unit_ids:
                continue
            utt_count = (await db.execute(
                select(func.count(Utterance.utterance_id)).where(Utterance.session_id == sid)
            )).scalar() or 0
            if utt_count >= 2:
                completed_unit_ids.add(unit_id)

    # 3. Build ordered list with sequential unlock logic
    # First unit is always unlocked. Each subsequent unit unlocks when the previous is completed.
    difficulty_map = {1: "쉬움", 2: "보통", 3: "어려움"}
    theme_week_emojis = {
        "earth_crew": {1: "🚀", 2: "🔍", 3: "💜", 4: "🎭"},
        "kpop_hunters": {1: "🎤", 2: "🎵", 3: "💖", 4: "🌟"},
        "dino_expedition": {1: "🦕", 2: "🦴", 3: "💚", 4: "🎒"},
    }
    week_emojis = theme_week_emojis.get(story_theme, {1: "🚀", 2: "🔍", 3: "💜", 4: "🎭"})

    response = []
    prev_completed = True  # First unit should be unlocked

    for idx, unit in enumerate(units):
        unit_id = unit.curriculum_unit_id
        is_completed = unit_id in completed_unit_ids

        if is_completed:
            status = "completed"
        elif prev_completed:
            status = "unlocked"
        else:
            status = "locked"

        response.append(AdventureSummary(
            session_id=unit_id,
            title=unit.title,
            emoji=week_emojis.get(unit.week, "🚀"),
            status=status,
            difficulty=difficulty_map.get(unit.difficulty_level, "보통"),
            week=unit.week or 1,
            order=idx,
            earned_stars=10 if is_completed else None,
            earned_xp=50 if is_completed else None,
        ))

        prev_completed = is_completed

    return response

@router.get("/{id}")
async def get_adventure_detail(
    id: str,
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    # 1. Get Unit
    stmt = select(CurriculumUnit).where(CurriculumUnit.curriculum_unit_id == id)
    result = await db.execute(stmt)
    unit = result.scalar_one_or_none()
    
    if not unit:
        raise HTTPException(status_code=404, detail="Adventure not found")
    
    # 2. Get Activities
    activity_stmt = select(Activity).where(
        Activity.curriculum_unit_id == id
    ).order_by(Activity.activity_id)
    activity_result = await db.execute(activity_stmt)
    activities = activity_result.scalars().all()
    
    # Return structure matching frontend expectation
    # Maps difficulty int 1-3 to string
    difficulty_map = ["쉬움", "보통", "어려움"]
    difficulty_str = difficulty_map[min(unit.difficulty_level - 1, 2)]
    
    return {
        "id": unit.curriculum_unit_id,
        "title": unit.title,
        "description": unit.description,
        "emoji": "🚀",
        "difficulty": difficulty_str,
        "duration": 600, # 10 mins
        "rewards": {"stars": 10, "xp": 50},
        "languageMode": unit.language_mode,
        "koreanRatio": unit.korean_ratio,
        "activities": [
            {
                "activityId": a.activity_id,
                "name": a.name,
                "activityType": a.activity_type,
                "introNarratorScript": a.intro_narrator_script,
                "outroNarratorScript": a.outro_narrator_script,
                "estimatedDurationMinutes": a.estimated_duration_minutes,
            }
            for a in activities
        ]
    }

@router.post("/{id}/complete")
async def complete_adventure(
    id: str,
    req: AdventureCompleteRequest,
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    # 1. Update Inventory
    stmt = select(ChildInventory).where(ChildInventory.child_id == child_id)
    result = await db.execute(stmt)
    inventory = result.scalar_one_or_none()

    if inventory:
        inventory.stars += req.stars
        inventory.xp = (inventory.child.xp or 0) + req.xp

    # 2. Update Child XP
    child_stmt = select(Child).where(Child.child_id == child_id)
    child_result = await db.execute(child_stmt)
    child = child_result.scalar_one()
    child.xp += req.xp

    await db.commit()

    return {"status": "success"}


@router.post("/{id}/skip")
async def skip_adventure(
    id: str,
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db),
):
    """Skip a locked adventure by spending stars."""
    # 1. Verify the unit exists
    unit = (await db.execute(
        select(CurriculumUnit).where(CurriculumUnit.curriculum_unit_id == id)
    )).scalar_one_or_none()
    if not unit:
        raise HTTPException(status_code=404, detail="Adventure not found")

    # 2. Check not already completed — end any active sessions for this unit
    existing_ended = (await db.execute(
        select(Session).where(
            and_(Session.child_id == child_id, Session.curriculum_unit_id == id, Session.status == "ended")
        )
    )).scalar_one_or_none()
    if existing_ended:
        raise HTTPException(status_code=400, detail="Adventure already completed")

    # End any active sessions for this unit (cleanup)
    active_sessions = (await db.execute(
        select(Session).where(
            and_(Session.child_id == child_id, Session.curriculum_unit_id == id, Session.status == "active")
        )
    )).scalars().all()
    for s in active_sessions:
        s.status = "ended"
        s.end_time = datetime.utcnow()
        s.duration_seconds = 0

    # 3. Check stars balance
    inventory = (await db.execute(
        select(ChildInventory).where(ChildInventory.child_id == child_id)
    )).scalar_one_or_none()
    if not inventory or inventory.stars < SKIP_COST_STARS:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough stars. Need {SKIP_COST_STARS}, have {inventory.stars if inventory else 0}",
        )

    # 4. Deduct stars
    inventory.stars -= SKIP_COST_STARS

    # 5. Create a skipped session so sequential unlock treats it as completed
    skipped_session = Session(
        child_id=child_id,
        session_type="curriculum",
        curriculum_unit_id=id,
        status="ended",
        end_time=datetime.utcnow(),
        duration_seconds=0,
    )
    db.add(skipped_session)
    await db.commit()

    logger.info(f"Child {child_id} skipped adventure {id} for {SKIP_COST_STARS} stars")

    return {
        "status": "skipped",
        "stars_spent": SKIP_COST_STARS,
        "remaining_stars": inventory.stars,
    }
