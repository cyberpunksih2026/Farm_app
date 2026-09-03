from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.order import Order
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(Order)

    def get_with_details(self, db: Session, order_id: int) -> Optional[Order]:
        return db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.delivery_address),
            joinedload(Order.payment),
            joinedload(Order.delivery)
        ).filter(Order.id == order_id).first()

    def get_by_order_number(self, db: Session, order_number: str) -> Optional[Order]:
        return db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.delivery_address),
            joinedload(Order.payment),
            joinedload(Order.delivery)
        ).filter(Order.order_number == order_number).first()

    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[Order]:
        return db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.delivery_address)
        ).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()


order_repo = OrderRepository()
