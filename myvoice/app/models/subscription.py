"""SubscriptionPlan & Subscription models (FDD 3.1.2)"""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_name: Mapped[str] = mapped_column(String(50))
    monthly_price: Mapped[float] = mapped_column(Numeric(10, 2))
    allowed_sessions_per_week: Mapped[int] = mapped_column(Integer)
    report_type: Mapped[str] = mapped_column(String(50))


class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("family_accounts.family_id"))
    plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("subscription_plans.plan_id"))
    status: Mapped[str] = mapped_column(String(30), default="trial")
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    billing_cycle: Mapped[str | None] = mapped_column(String(20), nullable=True, default="monthly")
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    family = relationship("FamilyAccount", back_populates="subscriptions")
