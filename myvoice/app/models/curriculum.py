"""CurriculumUnit, Activity, TaskDefinition models (FDD 3.1.7)"""
import uuid
from sqlalchemy import String, Integer, Float, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CurriculumUnit(Base):
    __tablename__ = "curriculum_units"

    curriculum_unit_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    phase: Mapped[int | None] = mapped_column(Integer, nullable=True)
    week: Mapped[int | None] = mapped_column(Integer, nullable=True)
    age_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    age_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    target_skills: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)
    language_mode: Mapped[str] = mapped_column(String(20), default="mixed")
    clumsiness_level: Mapped[int] = mapped_column(Integer, default=80)
    korean_ratio: Mapped[int] = mapped_column(Integer, default=50)
    story_theme: Mapped[str] = mapped_column(String(50), default="earth_crew")


class Activity(Base):
    __tablename__ = "activities"

    activity_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    curriculum_unit_id: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(200))
    activity_type: Mapped[str] = mapped_column(String(30))
    target_skills: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    instructions_for_ai: Mapped[str | None] = mapped_column(Text, nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(20), nullable=True)
    estimated_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # NEW: Narrator-Protagonist Structure (FDD 3.1.7.1)
    intro_narrator_script: Mapped[str | None] = mapped_column(Text, nullable=True)
    outro_narrator_script: Mapped[str | None] = mapped_column(Text, nullable=True)
    transition_trigger: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # NEW: Story Factory Integration (Phase 4B)
    story_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    key_expression: Mapped[str | None] = mapped_column(String(200), nullable=True)
    image_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_path: Mapped[str | None] = mapped_column(Text, nullable=True) # Local path to image


class TaskDefinition(Base):
    __tablename__ = "task_definitions"

    task_definition_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id: Mapped[str] = mapped_column(String(100))
    prompt_template: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_response_pattern: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_skill_ids: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)
