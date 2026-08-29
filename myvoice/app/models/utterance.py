"""Utterance model (FDD 3.1.4)"""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, Float, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Utterance(Base):
    __tablename__ = "utterances"

    utterance_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.session_id"))
    session_activity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    turn_index: Mapped[int] = mapped_column(Integer)
    speaker_type: Mapped[str] = mapped_column(String(10))
    text_raw: Mapped[str | None] = mapped_column(Text, nullable=True)
    text_normalized: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str | None] = mapped_column(String(10), nullable=True)
    dominant_language: Mapped[str | None] = mapped_column(String(10), nullable=True)
    language_mix_ratio_ko: Mapped[float | None] = mapped_column(Float, nullable=True)
    language_mix_ratio_en: Mapped[float | None] = mapped_column(Float, nullable=True)
    word_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unique_word_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    avg_sentence_length: Mapped[float | None] = mapped_column(Float, nullable=True)
    pronunciation_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    fluency_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    emotion_label: Mapped[str | None] = mapped_column(String(30), nullable=True)
    utterance_role: Mapped[str | None] = mapped_column(String(30), nullable=True)
    expected_child_response_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    stt_engine: Mapped[str | None] = mapped_column(String(50), nullable=True)
    stt_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("Session", back_populates="utterances")
