"""Shop & Inventory models (Phase 3)"""
import uuid
from datetime import date, datetime
from sqlalchemy import String, Integer, ForeignKey, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ShopItem(Base):
    __tablename__ = "shop_items"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g., "hint", "time_extension"
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    emoji: Mapped[str] = mapped_column(String(10))
    price: Mapped[int] = mapped_column(Integer)
    item_type: Mapped[str] = mapped_column(String(50))  # "consumable" or "permanent"


class ChildInventory(Base):
    __tablename__ = "child_inventories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("children.child_id"), unique=True)
    
    stars: Mapped[int] = mapped_column(Integer, default=0)

    # Owned skins (comma-separated IDs)
    owned_skins: Mapped[str] = mapped_column(String(500), default="")
    active_popo_skin: Mapped[str | None] = mapped_column(String(50), nullable=True)
    active_luna_skin: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    # Activity
    streak: Mapped[int] = mapped_column(Integer, default=0)
    last_active_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Passive star regeneration
    last_star_regen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    child = relationship("Child", back_populates="inventory")  # Need to add to Child
