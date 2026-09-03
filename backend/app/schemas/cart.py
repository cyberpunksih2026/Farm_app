from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.product import ProductResponse


class CartItemAddRequest(BaseModel):
    product_id: int
    quantity: float = Field(default=1.0, gt=0)


class CartItemUpdateRequest(BaseModel):
    quantity: float = Field(..., gt=0)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: float
    unit_price: float
    subtotal: float
    product: Optional[ProductResponse] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    items: List[CartItemResponse] = []
    item_count: int = 0
    subtotal: float = 0.0
    farmer_total: float = 0.0
    market_total: float = 0.0
    savings: float = 0.0
    delivery_fee: float = 0.0
    total_amount: float = 0.0

    model_config = ConfigDict(from_attributes=True)
