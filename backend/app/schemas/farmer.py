from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class FarmerBase(BaseModel):
    farmer_code: str = Field(..., min_length=2, max_length=20)
    name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=120)
    location: str = Field(..., min_length=2, max_length=100)
    state: str = Field(default="Tamil Nadu", max_length=50)
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    farm_size_acres: Optional[float] = None
    verification_status: str = "VERIFIED"
    is_active: bool = True
    bio: Optional[str] = None


class FarmerCreate(FarmerBase):
    pass


class FarmerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    farm_size_acres: Optional[float] = None
    verification_status: Optional[str] = None
    is_active: Optional[bool] = None
    bio: Optional[str] = None


class FarmerResponse(FarmerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
