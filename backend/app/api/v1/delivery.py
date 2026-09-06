from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.delivery import DeliveryAssignRequest, DeliveryStatusUpdateRequest, DeliveryResponse
from app.schemas.common import APIResponse
from app.services.delivery_service import DeliveryService
from app.api.v1.deps import require_employee, require_admin, get_current_user

router = APIRouter(prefix="/delivery", tags=["Delivery & Logistics"])


@router.get("/order/{order_id}", response_model=APIResponse[DeliveryResponse])
def get_order_delivery(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delivery = DeliveryService.get_by_order_id(db, order_id)
    return APIResponse(
        success=True,
        message="Delivery tracking details",
        data=DeliveryResponse.model_validate(delivery)
    )


@router.get("/track/{tracking_number}", response_model=APIResponse[DeliveryResponse])
def track_delivery(
    tracking_number: str,
    db: Session = Depends(get_db)
):
    delivery = DeliveryService.get_by_tracking_number(db, tracking_number)
    return APIResponse(
        success=True,
        message="Tracking status retrieved",
        data=DeliveryResponse.model_validate(delivery)
    )


@router.post("/order/{order_id}/assign", response_model=APIResponse[DeliveryResponse])
def assign_delivery_partner(
    order_id: int,
    assign_in: DeliveryAssignRequest,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    delivery = DeliveryService.assign_delivery(db, order_id, assign_in)
    return APIResponse(
        success=True,
        message=f"Order assigned to delivery partner {assign_in.employee_id}",
        data=DeliveryResponse.model_validate(delivery)
    )


@router.patch("/order/{order_id}/status", response_model=APIResponse[DeliveryResponse])
def update_delivery_status(
    order_id: int,
    status_in: DeliveryStatusUpdateRequest,
    employee: User = Depends(require_employee),
    db: Session = Depends(get_db)
):
    delivery = DeliveryService.update_delivery_status(db, order_id, status_in, employee)
    return APIResponse(
        success=True,
        message=f"Delivery status updated to {delivery.status}",
        data=DeliveryResponse.model_validate(delivery)
    )
