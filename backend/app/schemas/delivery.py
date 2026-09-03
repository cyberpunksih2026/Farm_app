from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class DeliveryAssignRequest(BaseModel):
    employee_id: int
    estimated_delivery: Optional[datetime] = None
    notes: Optional[str] = None


class DeliveryStatusUpdateRequest(BaseModel):
    status: str = Field(..., description="Target DeliveryStatus: PENDING, ASSIGNED, PICKED_UP, IN_TRANSIT, DELIVERED, FAILED")
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    notes: Optional[str] = None


class DeliveryResponse(BaseModel):
    id: int
    order_id: int
    employee_id: Optional[int] = None
    tracking_number: str
    status: str
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    estimated_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
