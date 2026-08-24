"""Vocabulary models (Phase 3)"""
import uuid
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class VocabularyCategory(Base):
    __tablename__ = "vocabulary_categories"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g., "food", "animals"
    name: Mapped[str] = mapped_column(String(100))
    emoji: Mapped[str] = mapped_column(String(10))
    total_words: Mapped[int] = mapped_column(Integer, default=0)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    words = relationship("VocabularyWord", back_populates="category", cascade="all, delete-orphan")
    progress = relationship("VocabularyProgress", back_populates="category")


class VocabularyWord(Base):
    __tablename__ = "vocabulary_words"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[str] = mapped_column(String(50), ForeignKey("vocabulary_categories.id"))
    word: Mapped[str] = mapped_column(String(100))
    korean: Mapped[str] = mapped_column(String(100))
    emoji: Mapped[str] = mapped_column(String(10))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    category = relationship("VocabularyCategory", back_populates="words")


class VocabularyProgress(Base):
    __tablename__ = "vocabulary_progress"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("children.child_id"))
    category_id: Mapped[str] = mapped_column(String(50), ForeignKey("vocabulary_categories.id"))
    words_learned: Mapped[int] = mapped_column(Integer, default=0)
    last_learned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    child = relationship("Child", back_populates="vocabulary_progress")  # Need to add to Child
    category = relationship("VocabularyCategory", back_populates="progress")
