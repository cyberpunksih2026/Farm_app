from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.payment import Payment, PaymentState
from app.models.order import Order, OrderStatus, PaymentStatus
from app.schemas.payment import PaymentProcessRequest


class PaymentService:
    @staticmethod
    def process_payment(db: Session, pay_data: PaymentProcessRequest) -> Payment:
        payment = db.query(Payment).filter(Payment.order_id == pay_data.order_id).first()
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment record for order not found")

        order = db.query(Order).filter(Order.id == pay_data.order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        if pay_data.simulate_success:
            payment.payment_status = PaymentState.COMPLETED
            payment.payment_method = pay_data.payment_method.upper()
            if pay_data.transaction_id:
                payment.transaction_id = pay_data.transaction_id

            order.payment_status = PaymentStatus.PAID
            if order.status == OrderStatus.CREATED:
                order.status = OrderStatus.CONFIRMED
        else:
            payment.payment_status = PaymentState.FAILED
            order.payment_status = PaymentStatus.FAILED

        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_by_order_id(db: Session, order_id: int) -> Payment:
        payment = db.query(Payment).filter(Payment.order_id == order_id).first()
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment record not found")
        return payment
