"""Report request/response schemas."""
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
import uuid


class ReportSkillSummaryResponse(BaseModel):
    skill_id: str
    skill_name: Optional[str] = None
    level: Optional[int] = None
    summary_for_parent: Optional[str] = None

    model_config = {"from_attributes": True}


class ReportResponse(BaseModel):
    report_id: uuid.UUID
    period_start_date: datetime
    period_end_date: datetime
    created_at: datetime
    summary_text: Optional[str] = None
    strengths_summary: Optional[str] = None
    areas_to_improve: Optional[str] = None
    recommendations_next_month: Optional[str] = None
    skill_summaries: List[ReportSkillSummaryResponse] = []

    model_config = {"from_attributes": True}
