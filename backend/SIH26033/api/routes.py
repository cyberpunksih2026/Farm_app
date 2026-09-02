from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from data.farmers import farmers
from logistics.logistics_engine import process_order

router = APIRouter(prefix="/api/logistics", tags=["Logistics"])


class BuyerRequest(BaseModel):
    id: str = "B001"
    name: str = "Puducherry Hotel"
    crop: str = Field(min_length=1)
    required_quantity: float = Field(gt=0)
    location: str = Field(min_length=1)
    latitude: float
    longitude: float


@router.post("/match")
def match_order(buyer: BuyerRequest):
    try:
        return process_order(farmers, buyer.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
