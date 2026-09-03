from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.payment import PaymentProcessRequest, PaymentResponse
from app.schemas.common import APIResponse
from app.services.payment_service import PaymentService
from app.api.v1.deps import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/process", response_model=APIResponse[PaymentResponse])
def process_payment(
    pay_data: PaymentProcessRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    payment = PaymentService.process_payment(db, pay_data)
    return APIResponse(
        success=True,
        message=f"Payment status: {payment.payment_status}",
        data=PaymentResponse.model_validate(payment)
    )


@router.get("/order/{order_id}", response_model=APIResponse[PaymentResponse])
def get_order_payment(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    payment = PaymentService.get_by_order_id(db, order_id)
    return APIResponse(
        success=True,
        message="Payment details retrieved",
        data=PaymentResponse.model_validate(payment)
    )
