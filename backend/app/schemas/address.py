from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class AddressBase(BaseModel):
    recipient_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    street: str = Field(..., min_length=5, max_length=255)
    landmark: Optional[str] = None
    city: str = Field(..., min_length=2, max_length=50)
    state: str = Field(default="Tamil Nadu", max_length=50)
    postal_code: str = Field(..., min_length=5, max_length=20)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    recipient_name: Optional[str] = None
    phone: Optional[str] = None
    street: Optional[str] = None
    landmark: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: Optional[bool] = None


class AddressResponse(AddressBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
