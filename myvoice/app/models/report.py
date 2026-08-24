"""Report & ReportSkillSummary models (FDD 3.1.8)"""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("children.child_id"))
    family_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("family_accounts.family_id"))
    period_start_date: Mapped[datetime] = mapped_column(DateTime)
    period_end_date: Mapped[datetime] = mapped_column(DateTime)
    report_type: Mapped[str] = mapped_column(String(50), default="pdf_basic")
    template_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    locale: Mapped[str] = mapped_column(String(10), default="ko_KR")
    summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    strengths_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    areas_to_improve: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommendations_next_month: Mapped[str | None] = mapped_column(Text, nullable=True)
    delivery_channel: Mapped[str | None] = mapped_column(String(30), nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    skill_summaries = relationship("ReportSkillSummary", back_populates="report", lazy="selectin")


class ReportSkillSummary(Base):
    __tablename__ = "report_skill_summaries"

    report_skill_summary_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reports.report_id"))
    skill_id: Mapped[str] = mapped_column(String(100))
    level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    summary_for_parent: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    report = relationship("Report", back_populates="skill_summaries")
