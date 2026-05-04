"""Children router: CRUD for child profiles."""
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.family import Child
from app.schemas.child import ChildCreate, ChildResponse
from app.core.security import get_current_family_id

router = APIRouter()


@router.post("", response_model=ChildResponse, status_code=201)
async def create_child(
    req: ChildCreate,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    child = Child(
        family_id=uuid.UUID(family_id),
        name=req.name,
        birth_date=datetime.combine(req.birth_date, datetime.min.time()),
        gender=req.gender,
        primary_language=req.primary_language,
        development_stage_language=req.development_stage_language,
    )
    db.add(child)
    await db.flush()
    return child


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child(
    child_id: uuid.UUID,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Child).where(Child.child_id == child_id, Child.family_id == uuid.UUID(family_id))
    )
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child
