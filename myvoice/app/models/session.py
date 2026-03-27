"""Session & SessionActivity models (FDD 3.1.3)"""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, Float, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("children.child_id"))
    subscription_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("subscriptions.subscription_id"), nullable=True)
    session_type: Mapped[str] = mapped_column(String(20), default="curriculum")
    language_mode: Mapped[str] = mapped_column(String(20), default="mixed")
    curriculum_unit_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="idle")
    engagement_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    attention_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    emotional_state_overall: Mapped[str | None] = mapped_column(String(30), nullable=True)
    raw_audio_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    stt_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    flag_for_expert_review: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    child = relationship("Child", back_populates="sessions")
    activities = relationship("SessionActivity", back_populates="session", lazy="selectin")
    utterances = relationship("Utterance", back_populates="session", lazy="selectin")


class SessionActivity(Base):
    __tablename__ = "session_activities"

    session_activity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.session_id"))
    activity_id: Mapped[str] = mapped_column(String(100))
    order_index: Mapped[int] = mapped_column(Integer)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="idle")

    # Relationships
    session = relationship("Session", back_populates="activities")
