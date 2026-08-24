"""Parent-scoped children router: CRUD for child profiles."""
import uuid
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.family import Child
from app.schemas.child import ChildCreate, ChildResponse, ChildUpdate
from app.core.security import get_current_family_id, hash_password

router = APIRouter()


@router.post("", response_model=ChildResponse, status_code=201)
async def create_child(
    req: ChildCreate,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    """Parent View: 아이 프로필을 생성합니다."""
    # Convert age to birth_date if provided
    if req.age is not None and req.birth_date is None:
        today = date.today()
        birth_date = date(today.year - req.age, today.month, today.day)
    else:
        birth_date = req.birth_date or date.today()

    child = Child(
        family_id=uuid.UUID(family_id),
        name=req.name,
        birth_date=datetime.combine(birth_date, datetime.min.time()),
        gender=req.gender,
        primary_language=req.primary_language,
        development_stage_language=req.development_stage_language,
        preferences_topics={"interests": req.interests} if req.interests else None,
    )
    # PIN 설정 (선택)
    if req.pin:
        child.pin_hash = hash_password(req.pin)
    db.add(child)
    await db.flush()
    return child


@router.get("", response_model=list[ChildResponse])
async def list_children(
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    """Parent View: 가족의 모든 아이 프로필 목록을 조회합니다."""
    result = await db.execute(
        select(Child).where(Child.family_id == uuid.UUID(family_id))
    )
    return result.scalars().all()


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child(
    child_id: uuid.UUID,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    """Parent View: 특정 아이의 프로필을 조회합니다."""
    result = await db.execute(
        select(Child).where(
            Child.child_id == child_id,
            Child.family_id == uuid.UUID(family_id),
        )
    )
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


@router.patch("/{child_id}", response_model=ChildResponse)
async def update_child(
    child_id: uuid.UUID,
    req: ChildUpdate,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    """Parent View: 아이 프로필을 수정합니다."""
    # 1. Fetch Child
    result = await db.execute(
        select(Child).where(
            Child.child_id == child_id,
            Child.family_id == uuid.UUID(family_id),
        )
    )
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    # 2. Update Fields
    if req.name is not None:
        child.name = req.name
    if req.age is not None and req.birth_date is None:
        child.birth_date = datetime.combine(
            date(date.today().year - req.age, 1, 1), datetime.min.time()
        )
    elif req.birth_date is not None:
        child.birth_date = datetime.combine(req.birth_date, datetime.min.time())
    if req.gender is not None:
        child.gender = req.gender
    if req.interests is not None:
        child.preferences_topics = {"interests": req.interests}
    if req.primary_language is not None:
        child.primary_language = req.primary_language
    if req.development_stage_language is not None:
        child.development_stage_language = req.development_stage_language
    if req.avatar_id is not None:
        child.avatar_id = req.avatar_id
    if req.pin is not None:
        child.pin_hash = hash_password(req.pin)

    # 3. Save
    db.add(child)
    await db.commit()
    await db.refresh(child)
    return child
