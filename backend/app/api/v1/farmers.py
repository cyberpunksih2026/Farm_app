from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.farmer import Farmer
from app.models.user import User
from app.schemas.farmer import FarmerCreate, FarmerUpdate, FarmerResponse
from app.schemas.common import APIResponse
from app.services.farmer_service import FarmerService
from app.api.v1.deps import require_admin

router = APIRouter(prefix="/farmers", tags=["Farmers"])


@router.get("", response_model=APIResponse[List[FarmerResponse]])
def list_farmers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    farmers = FarmerService.get_all(db, skip=skip, limit=limit)
    return APIResponse(
        success=True,
        message="Farmers list retrieved successfully",
        data=[FarmerResponse.model_validate(f) for f in farmers]
    )


@router.get("/{farmer_id}", response_model=APIResponse[FarmerResponse])
def get_farmer(
    farmer_id: int,
    db: Session = Depends(get_db)
):
    farmer = FarmerService.get_by_id(db, farmer_id)
    return APIResponse(
        success=True,
        message="Farmer details retrieved",
        data=FarmerResponse.model_validate(farmer)
    )


@router.post("", response_model=APIResponse[FarmerResponse], status_code=status.HTTP_201_CREATED)
def create_farmer(
    farmer_in: FarmerCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    farmer = FarmerService.create(db, farmer_in)
    return APIResponse(
        success=True,
        message="Farmer profile created successfully",
        data=FarmerResponse.model_validate(farmer)
    )


@router.put("/{farmer_id}", response_model=APIResponse[FarmerResponse])
def update_farmer(
    farmer_id: int,
    farmer_update: FarmerUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    farmer = FarmerService.update(db, farmer_id, farmer_update)
    return APIResponse(
        success=True,
        message="Farmer profile updated successfully",
        data=FarmerResponse.model_validate(farmer)
    )
