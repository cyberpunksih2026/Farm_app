from typing import List, Optional
from pydantic import BaseModel, Field


class BuyerRequest(BaseModel):
    id: str = Field(default="B001", description="Buyer / Order reference ID")
    name: str = Field(default="Demo Customer", description="Buyer or institution name")
    crop: str = Field(..., min_length=1, description="Crop or produce requested (e.g. Tomato, Onion, Potato)")
    required_quantity: float = Field(..., gt=0, description="Quantity in kg required")
    location: str = Field(default="Puducherry", min_length=1)
    latitude: float = Field(..., description="Destination latitude coordinate")
    longitude: float = Field(..., description="Destination longitude coordinate")


class FarmerAllocation(BaseModel):
    farmer_id: int
    farmer_code: str
    farmer_name: str
    crop: str
    location: str
    allocated_quantity: float
    distance_km: float
    price_per_kg: float
    total_cost: float


class LogisticsResult(BaseModel):
    buyer_id: str
    buyer_name: str
    crop: str
    required_quantity: float
    collected_quantity: float
    shortage: float
    status: str  # "fulfilled" or "shortage"
    total_farmers_matched: int
    farmers: List[FarmerAllocation]
