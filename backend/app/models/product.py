from datetime import date
from typing import Optional, List
from sqlalchemy import String, Float, Text, Boolean, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class ProductUnit:
    KG = "kg"
    GRAM = "g"
    PIECE = "piece"
    BUNCH = "bunch"
    LITER = "L"


class ProductStatus:
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    farmer_id: Mapped[int] = mapped_column(Integer, ForeignKey("farmers.id", ondelete="CASCADE"), index=True, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), index=True, nullable=False)
    
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    unit: Mapped[str] = mapped_column(String(20), default=ProductUnit.KG, nullable=False)
    
    # Transparent pricing
    base_price: Mapped[float] = mapped_column(Float, nullable=False)        # App display price
    farmer_price: Mapped[float] = mapped_column(Float, nullable=False)      # Paid to farmer
    market_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # General retail comparison
    
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_organic: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    harvest_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default=ProductStatus.ACTIVE, index=True, nullable=False)

    # Relationships
    farmer = relationship("Farmer", back_populates="products")
    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False, cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product")
