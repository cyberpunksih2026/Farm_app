from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.delivery import Delivery, DeliveryStatus
from app.models.order import Order, OrderStatus
from app.models.user import User, UserRole
from app.schemas.delivery import DeliveryAssignRequest, DeliveryStatusUpdateRequest


class DeliveryService:
    @staticmethod
    def get_by_order_id(db: Session, order_id: int) -> Delivery:
        delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
        if not delivery:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery record not found")
        return delivery

    @staticmethod
    def get_by_tracking_number(db: Session, tracking_number: str) -> Delivery:
        delivery = db.query(Delivery).filter(Delivery.tracking_number == tracking_number).first()
        if not delivery:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking number not found")
        return delivery

    @staticmethod
    def assign_delivery(db: Session, order_id: int, assign_data: DeliveryAssignRequest) -> Delivery:
        delivery = DeliveryService.get_by_order_id(db, order_id)
        
        employee = db.query(User).filter(User.id == assign_data.employee_id).first()
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee user not found")

        delivery.employee_id = assign_data.employee_id
        delivery.status = DeliveryStatus.ASSIGNED
        if assign_data.estimated_delivery:
            delivery.estimated_delivery = assign_data.estimated_delivery
        if assign_data.notes:
            delivery.notes = assign_data.notes

        db.commit()
        db.refresh(delivery)
        return delivery

    @staticmethod
    def update_delivery_status(db: Session, order_id: int, status_data: DeliveryStatusUpdateRequest, current_user: User) -> Delivery:
        delivery = DeliveryService.get_by_order_id(db, order_id)

        if current_user.role == UserRole.EMPLOYEE and delivery.employee_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not assigned to this delivery")

        delivery.status = status_data.status
        if status_data.current_lat is not None:
            delivery.current_lat = status_data.current_lat
        if status_data.current_lng is not None:
            delivery.current_lng = status_data.current_lng
        if status_data.notes:
            delivery.notes = status_data.notes

        if status_data.status == DeliveryStatus.DELIVERED:
            delivery.actual_delivery = datetime.now(timezone.utc)
            order = db.query(Order).filter(Order.id == order_id).first()
            if order and order.status != OrderStatus.DELIVERED:
                order.status = OrderStatus.DELIVERED

        db.commit()
        db.refresh(delivery)
        return delivery
