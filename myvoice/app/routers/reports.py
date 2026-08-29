"""Reports router: list and detail."""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.report import Report
from app.schemas.report import ReportResponse
from app.core.security import get_current_family_id

router = APIRouter()


@router.get("", response_model=list[ReportResponse])
async def list_reports(
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Report).where(Report.family_id == uuid.UUID(family_id))
    )
    reports = result.scalars().all()
    return reports


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: uuid.UUID,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Report).where(Report.report_id == report_id, Report.family_id == uuid.UUID(family_id))
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
