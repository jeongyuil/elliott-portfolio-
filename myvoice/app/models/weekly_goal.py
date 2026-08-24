"""Weekly Goal models (Phase 3)"""
import uuid
from datetime import date
from sqlalchemy import Integer, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class WeeklyGoal(Base):
    __tablename__ = "weekly_goals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("children.child_id"))
    week_start: Mapped[date] = mapped_column(Date)
    
    # Targets & Progress
    xp_target: Mapped[int] = mapped_column(Integer, default=1000)
    xp_current: Mapped[int] = mapped_column(Integer, default=0)
    
    missions_target: Mapped[int] = mapped_column(Integer, default=7)
    missions_current: Mapped[int] = mapped_column(Integer, default=0)
    
    study_time_target: Mapped[int] = mapped_column(Integer, default=60)  # minutes
    study_time_current: Mapped[int] = mapped_column(Integer, default=0)
    
    words_target: Mapped[int] = mapped_column(Integer, default=20)
    words_current: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    child = relationship("Child", back_populates="weekly_goals")  # Need to add to Child
