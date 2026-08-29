"""FamilyAccount & Child models (FDD 3.1.1)"""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class FamilyAccount(Base):
    __tablename__ = "family_accounts"

    family_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_name: Mapped[str] = mapped_column(String(100))
    contact_email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Email verification
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verification_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email_verification_expires: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Password reset
    password_reset_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_reset_expires: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Parent mode PIN (4-digit, hashed)
    parent_mode_pin: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    children = relationship("Child", back_populates="family", lazy="selectin")
    subscriptions = relationship("Subscription", back_populates="family", lazy="selectin")
    oauth_accounts = relationship("OAuthAccount", back_populates="family", lazy="selectin")


class Child(Base):
    __tablename__ = "children"

    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("family_accounts.family_id"))
    name: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[datetime] = mapped_column(DateTime)
    gender: Mapped[str | None] = mapped_column(String(10), nullable=True)
    primary_language: Mapped[str] = mapped_column(String(10), default="ko")
    secondary_language: Mapped[str | None] = mapped_column(String(10), nullable=True, default="en")
    development_stage_language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    preferences_topics: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    pin_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    # Phase 3 Fields
    nickname: Mapped[str | None] = mapped_column(String(50), nullable=True)
    avatar_emoji: Mapped[str | None] = mapped_column(String(10), nullable=True)
    level: Mapped[int] = mapped_column(Integer, default=1)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    selected_story_theme: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Relationships
    family = relationship("FamilyAccount", back_populates="children")
    sessions = relationship("Session", back_populates="child", lazy="select")
    
    # Phase 3 Relationships
    inventory = relationship("ChildInventory", back_populates="child", uselist=False, lazy="selectin")
    weekly_goals = relationship("WeeklyGoal", back_populates="child", lazy="selectin")
    vocabulary_progress = relationship("VocabularyProgress", back_populates="child", lazy="selectin")
