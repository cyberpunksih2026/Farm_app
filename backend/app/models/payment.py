from typing import Optional
from sqlalchemy import String, Float, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class PaymentMethod:
    UPI = "UPI"
    CARD = "CARD"
    NETBANKING = "NETBANKING"
    COD = "COD"


class PaymentState:
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), default=PaymentMethod.UPI, nullable=False)
    payment_status: Mapped[str] = mapped_column(String(30), default=PaymentState.PENDING, index=True, nullable=False)
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True, nullable=True)
    gateway_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    order = relationship("Order", back_populates="payment")
