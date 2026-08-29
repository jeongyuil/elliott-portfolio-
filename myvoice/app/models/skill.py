"""Skill, SkillLevel, TaskAttempt models (FDD 3.1.5 & 3.1.6)"""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, Float, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    skill_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(30))
    mode: Mapped[str] = mapped_column(String(20))
    age_band: Mapped[str | None] = mapped_column(String(10), nullable=True)
    can_do_examples: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    skill_schema_version: Mapped[str] = mapped_column(String(10), default="v0.1")


class SkillLevel(Base):
    __tablename__ = "skill_levels"

    skill_level_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("children.child_id"))
    skill_id: Mapped[str] = mapped_column(String(100), ForeignKey("skills.skill_id"))
    snapshot_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    raw_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    level: Mapped[int] = mapped_column(Integer, default=1)
    percentile_by_age: Mapped[float | None] = mapped_column(Float, nullable=True)
    trend_direction: Mapped[str | None] = mapped_column(String(10), nullable=True)
    source: Mapped[str] = mapped_column(String(20), default="ai_auto")
    evaluation_method: Mapped[str] = mapped_column(String(30), default="rule_v0.1")
    evaluation_model_version: Mapped[str] = mapped_column(String(10), default="v0.1")
    skill_schema_version: Mapped[str] = mapped_column(String(10), default="v0.1")


class TaskAttempt(Base):
    __tablename__ = "task_attempts"

    task_attempt_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id: Mapped[str] = mapped_column(String(100))
    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("children.child_id"))
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.session_id"))
    task_definition_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    expected_response_pattern: Mapped[str | None] = mapped_column(Text, nullable=True)
    evaluated_correctness: Mapped[str | None] = mapped_column(String(30), nullable=True)
    related_utterance_ids: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    instruction_understood: Mapped[str | None] = mapped_column(String(15), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
