from typing import Optional, List
from sqlalchemy import String, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class OrderStatus:
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    PICKING = "PICKING"
    PACKED = "PACKED"
    READY_FOR_DISPATCH = "READY_FOR_DISPATCH"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    RETURNED = "RETURNED"

    VALID_TRANSITIONS = {
        CREATED: [CONFIRMED, CANCELLED, FAILED],
        CONFIRMED: [PICKING, CANCELLED],
        PICKING: [PACKED, CANCELLED],
        PACKED: [READY_FOR_DISPATCH, CANCELLED],
        READY_FOR_DISPATCH: [OUT_FOR_DELIVERY, CANCELLED],
        OUT_FOR_DELIVERY: [DELIVERED, RETURNED, FAILED],
        DELIVERED: [RETURNED],
        CANCELLED: [],
        FAILED: [],
        RETURNED: [],
    }

    @classmethod
    def can_transition(cls, from_status: str, to_status: str) -> bool:
        allowed = cls.VALID_TRANSITIONS.get(from_status, [])
        return to_status in allowed


class PaymentStatus:
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    delivery_address_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("addresses.id", ondelete="SET NULL"), nullable=True)
    
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)
    delivery_fee: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default=OrderStatus.CREATED, index=True, nullable=False)
    payment_status: Mapped[str] = mapped_column(String(20), default=PaymentStatus.PENDING, index=True, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="orders")
    delivery_address = relationship("Address", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")
    delivery = relationship("Delivery", back_populates="order", uselist=False, cascade="all, delete-orphan")


class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), index=True, nullable=False)
    product_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    farmer_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True)
    
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), default="kg", nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    farmer_price: Mapped[float] = mapped_column(Float, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
