from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.farmer import Farmer
from app.schemas.farmer import FarmerCreate, FarmerUpdate


class FarmerService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Farmer]:
        return db.query(Farmer).filter(Farmer.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, farmer_id: int) -> Farmer:
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")
        return farmer

    @staticmethod
    def create(db: Session, farmer_in: FarmerCreate) -> Farmer:
        existing = db.query(Farmer).filter(Farmer.farmer_code == farmer_in.farmer_code).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Farmer code already exists")
        
        farmer = Farmer(**farmer_in.model_dump())
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
        return farmer

    @staticmethod
    def update(db: Session, farmer_id: int, update_data: FarmerUpdate) -> Farmer:
        farmer = FarmerService.get_by_id(db, farmer_id)
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(farmer, field, value)
        db.commit()
        db.refresh(farmer)
        return farmer
