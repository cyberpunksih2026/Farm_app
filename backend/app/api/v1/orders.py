from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.order import OrderCreateRequest, OrderStatusUpdateRequest, OrderResponse
from app.schemas.common import APIResponse
from app.services.order_service import OrderService
from app.api.v1.deps import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=APIResponse[OrderResponse], status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = OrderService.create_order(db, current_user, order_in)
    return APIResponse(
        success=True,
        message="Order placed successfully",
        data=OrderResponse.model_validate(order)
    )


@router.get("", response_model=APIResponse[List[OrderResponse]])
def list_orders(
    status_filter: Optional[str] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = OrderService.list_orders(db, current_user, status_filter=status_filter, skip=skip, limit=limit)
    return APIResponse(
        success=True,
        message="Orders retrieved successfully",
        data=[OrderResponse.model_validate(o) for o in orders]
    )


@router.get("/{order_id}", response_model=APIResponse[OrderResponse])
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = OrderService.get_order_by_id(db, order_id, current_user)
    return APIResponse(
        success=True,
        message="Order details retrieved",
        data=OrderResponse.model_validate(order)
    )


@router.patch("/{order_id}/status", response_model=APIResponse[OrderResponse])
def update_order_status(
    order_id: int,
    status_in: OrderStatusUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = OrderService.update_order_status(db, order_id, status_in, current_user)
    return APIResponse(
        success=True,
        message=f"Order status updated to {order.status}",
        data=OrderResponse.model_validate(order)
    )
