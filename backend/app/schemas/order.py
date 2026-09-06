from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.address import AddressResponse


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: float = Field(..., gt=0)


class OrderCreateRequest(BaseModel):
    delivery_address_id: Optional[int] = None
    items: Optional[List[OrderItemCreate]] = None  # If empty, will create order from active cart
    payment_method: str = Field(default="UPI", description="UPI, CARD, NETBANKING, COD")
    notes: Optional[str] = None


class OrderStatusUpdateRequest(BaseModel):
    status: str = Field(..., description="Target OrderStatus according to state machine")
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: Optional[int] = None
    farmer_id: Optional[int] = None
    product_name: str
    quantity: float
    unit: str
    unit_price: float
    farmer_price: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int
    delivery_address_id: Optional[int] = None
    subtotal: float
    delivery_fee: float
    discount_amount: float
    total_amount: float
    status: str
    payment_status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    delivery_address: Optional[AddressResponse] = None

    model_config = ConfigDict(from_attributes=True)
