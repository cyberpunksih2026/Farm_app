from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class InventoryBase(BaseModel):
    stock_quantity: float = Field(..., ge=0)
    reserved_quantity: float = Field(default=0.0, ge=0)
    min_threshold: float = Field(default=5.0, ge=0)
    unit: str = "kg"


class InventoryUpdate(BaseModel):
    stock_quantity: Optional[float] = Field(None, ge=0)
    reserved_quantity: Optional[float] = Field(None, ge=0)
    min_threshold: Optional[float] = Field(None, ge=0)
    unit: Optional[str] = None


class InventoryResponse(InventoryBase):
    id: int
    product_id: int
    available_quantity: float
    last_restocked_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RestockRequest(BaseModel):
    quantity: float = Field(..., gt=0, description="Quantity to add to stock")
