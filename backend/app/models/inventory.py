from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Float, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Inventory(Base, TimestampMixin):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    
    stock_quantity: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reserved_quantity: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    min_threshold: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), default="kg", nullable=False)
    last_restocked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    product = relationship("Product", back_populates="inventory")

    @property
    def available_quantity(self) -> float:
        return max(0.0, self.stock_quantity - self.reserved_quantity)
