from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.farmer import Farmer
from app.repositories.base import BaseRepository


class FarmerRepository(BaseRepository[Farmer]):
    def __init__(self):
        super().__init__(Farmer)

    def get_by_code(self, db: Session, code: str) -> Optional[Farmer]:
        return db.query(Farmer).filter(Farmer.farmer_code == code).first()

    def get_active(self, db: Session) -> List[Farmer]:
        return db.query(Farmer).filter(Farmer.is_active == True).all()


farmer_repo = FarmerRepository()
