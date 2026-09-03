from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class PaymentProcessRequest(BaseModel):
    order_id: int
    payment_method: str = Field(default="UPI", description="UPI, CARD, NETBANKING, COD")
    transaction_id: Optional[str] = None
    simulate_success: bool = True


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
