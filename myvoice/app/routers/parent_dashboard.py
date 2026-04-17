from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.core.security import get_current_family_id, hash_password, verify_password
from app.services.aggregation_service import AggregationService
from app.services.report_service import ReportService
from app.models import Child, Report, FamilyAccount

from app.schemas.report import ReportResponse


class PinSetRequest(BaseModel):
    pin: str = Field(..., min_length=4, max_length=4, pattern=r"^\d{4}$")

class PinVerifyRequest(BaseModel):
    pin: str = Field(..., min_length=4, max_length=4, pattern=r"^\d{4}$")

router = APIRouter(prefix="/parent", tags=["parent-dashboard"])

async def verify_child_ownership(db: AsyncSession, family_id: str, child_id: UUID) -> Child:
    stmt = select(Child).where(
        Child.child_id == child_id,
        Child.family_id == family_id
    )
    result = await db.execute(stmt)
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found or does not belong to this family")
    return child

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    child_id: UUID,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get weekly aggregated stats for the dashboard.
    """
    await verify_child_ownership(db, family_id, child_id)
    stats = await AggregationService.get_weekly_stats(db, child_id)
    return stats

@router.get("/reports", response_model=list[ReportResponse])
async def list_reports(
    child_id: UUID,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db)
):
    """
    List all reports for a child.
    """
    await verify_child_ownership(db, family_id, child_id)
    # Eager load skill_summaries if needed, but selectin load is default in model
    stmt = select(Report).where(Report.child_id == child_id).order_by(Report.created_at.desc())
    result = await db.execute(stmt)
    reports = result.scalars().all()
    return reports

@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report_detail(
    report_id: UUID,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed report with skill summaries.
    """
    # 1. Fetch Report
    stmt = select(Report).where(Report.report_id == report_id)
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    # 2. Verify Ownership
    if str(report.family_id) != family_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this report")
        
    return report

@router.post("/reports/generate")
async def generate_report_manually(
    child_id: UUID,
    year: int = Query(..., description="Report Year"),
    month: int = Query(..., description="Report Month"),
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Manually trigger report generation (Testing/Demo purpose).
    """
    await verify_child_ownership(db, family_id, child_id)
    report = await ReportService.generate_monthly_report(db, child_id, year, month)
    return report


# ── PIN Management ──────────────────────────────────────────────────

@router.get("/pin/status")
async def get_pin_status(
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    """Check whether a parent mode PIN has been set."""
    stmt = select(FamilyAccount).where(FamilyAccount.family_id == family_id)
    result = await db.execute(stmt)
    family = result.scalar_one_or_none()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return {"has_pin": family.parent_mode_pin is not None}


@router.post("/pin")
async def set_pin(
    body: PinSetRequest,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    """Set or update the 4-digit parent mode PIN."""
    stmt = select(FamilyAccount).where(FamilyAccount.family_id == family_id)
    result = await db.execute(stmt)
    family = result.scalar_one_or_none()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    family.parent_mode_pin = hash_password(body.pin)
    db.add(family)
    await db.flush()
    return {"ok": True}


@router.post("/pin/verify")
async def verify_pin(
    body: PinVerifyRequest,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    """Verify the 4-digit parent mode PIN."""
    stmt = select(FamilyAccount).where(FamilyAccount.family_id == family_id)
    result = await db.execute(stmt)
    family = result.scalar_one_or_none()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    if not family.parent_mode_pin:
        raise HTTPException(status_code=400, detail="PIN not set")
    if not verify_password(body.pin, family.parent_mode_pin):
        raise HTTPException(status_code=401, detail="Incorrect PIN")
    return {"ok": True}
