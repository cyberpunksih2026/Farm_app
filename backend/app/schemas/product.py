from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.farmer import FarmerResponse
from app.schemas.category import CategoryResponse
from app.schemas.inventory import InventoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = None
    unit: str = "kg"
    base_price: float = Field(..., gt=0, description="Customer selling price")
    farmer_price: float = Field(..., gt=0, description="Direct price paid to farmer")
    market_price: Optional[float] = Field(None, gt=0, description="Traditional retail market price for price transparency comparison")
    image_url: Optional[str] = None
    is_organic: bool = False
    harvest_date: Optional[date] = None
    status: str = "ACTIVE"


class ProductCreate(ProductBase):
    farmer_id: int
    category_id: int
    initial_stock: Optional[float] = Field(default=0.0, ge=0)


class ProductUpdate(BaseModel):
    farmer_id: Optional[int] = None
    category_id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    base_price: Optional[float] = Field(None, gt=0)
    farmer_price: Optional[float] = Field(None, gt=0)
    market_price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    is_organic: Optional[bool] = None
    harvest_date: Optional[date] = None
    status: Optional[str] = None


class ProductResponse(ProductBase):
    id: int
    farmer_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    inventory: Optional[InventoryResponse] = None

    model_config = ConfigDict(from_attributes=True)


class ProductDetailResponse(ProductResponse):
    farmer: Optional[FarmerResponse] = None
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)
