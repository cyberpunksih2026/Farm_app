import random
import string
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.order import Order, OrderItem, OrderStatus, PaymentStatus
from app.models.product import Product, ProductStatus
from app.models.inventory import Inventory
from app.models.cart import Cart, CartItem
from app.models.payment import Payment, PaymentMethod, PaymentState
from app.models.delivery import Delivery, DeliveryStatus
from app.models.user import User, UserRole
from app.schemas.order import OrderCreateRequest, OrderStatusUpdateRequest
from app.services.inventory_service import InventoryService


def generate_order_number() -> str:
    date_part = datetime.now(timezone.utc).strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"FARM-{date_part}-{random_part}"


def generate_tracking_number() -> str:
    random_digits = ''.join(random.choices(string.digits, k=8))
    return f"TRK-{random_digits}"


class OrderService:
    @staticmethod
    def create_order(db: Session, user: User, order_in: OrderCreateRequest) -> Order:
        order_items_to_create = []

        if order_in.items and len(order_in.items) > 0:
            for it in order_in.items:
                product = db.query(Product).options(joinedload(Product.inventory)).filter(Product.id == it.product_id).first()
                if not product or product.status != ProductStatus.ACTIVE:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product {it.product_id} is unavailable")
                order_items_to_create.append((product, it.quantity))
        else:
            cart = db.query(Cart).options(
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.inventory)
            ).filter(Cart.user_id == user.id).first()
            if not cart or not cart.items:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty. Cannot checkout.")
            for ci in cart.items:
                if ci.product.status != ProductStatus.ACTIVE:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product {ci.product.name} is currently unavailable")
                order_items_to_create.append((ci.product, ci.quantity))

        for product, qty in order_items_to_create:
            InventoryService.reserve_stock(db, product.id, qty)

        subtotal = 0.0
        for product, qty in order_items_to_create:
            subtotal += round(product.base_price * qty, 2)

        subtotal = round(subtotal, 2)
        delivery_fee = 0.0 if subtotal >= 299.0 else 35.0
        discount = 0.0
        total_amount = round(subtotal + delivery_fee - discount, 2)

        order_number = generate_order_number()
        order = Order(
            order_number=order_number,
            user_id=user.id,
            delivery_address_id=order_in.delivery_address_id,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            discount_amount=discount,
            total_amount=total_amount,
            status=OrderStatus.CREATED,
            payment_status=PaymentStatus.PENDING,
            notes=order_in.notes
        )
        db.add(order)
        db.flush()

        for product, qty in order_items_to_create:
            item_subtotal = round(product.base_price * qty, 2)
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                farmer_id=product.farmer_id,
                product_name=product.name,
                quantity=qty,
                unit=product.unit,
                unit_price=product.base_price,
                farmer_price=product.farmer_price,
                subtotal=item_subtotal
            )
            db.add(order_item)

        payment = Payment(
            order_id=order.id,
            amount=total_amount,
            payment_method=order_in.payment_method.upper(),
            payment_status=PaymentState.PENDING,
            transaction_id=f"TXN-{order_number}"
        )
        db.add(payment)

        delivery = Delivery(
            order_id=order.id,
            tracking_number=generate_tracking_number(),
            status=DeliveryStatus.PENDING
        )
        db.add(delivery)

        cart = db.query(Cart).filter(Cart.user_id == user.id).first()
        if cart:
            db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_order_by_id(db: Session, order_id: int, current_user: User) -> Order:
        order = db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.delivery_address),
            joinedload(Order.payment),
            joinedload(Order.delivery)
        ).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        if current_user.role == UserRole.CUSTOMER and order.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this order")

        return order

    @staticmethod
    def list_orders(
        db: Session,
        current_user: User,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Order]:
        q = db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.delivery_address)
        )

        if current_user.role == UserRole.CUSTOMER:
            q = q.filter(Order.user_id == current_user.id)
        elif status_filter:
            q = q.filter(Order.status == status_filter)

        return q.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_order_status(db: Session, order_id: int, update_in: OrderStatusUpdateRequest, current_user: User) -> Order:
        order = db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.delivery)
        ).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        if current_user.role == UserRole.CUSTOMER:
            if order.user_id != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
            if update_in.status != OrderStatus.CANCELLED:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Customers can only cancel active orders")

        if not OrderStatus.can_transition(order.status, update_in.status):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid state transition from {order.status} to {update_in.status}"
            )

        old_status = order.status
        order.status = update_in.status
        if update_in.notes:
            order.notes = (order.notes or "") + f"\n[{datetime.now(timezone.utc).isoformat()}] {update_in.notes}"

        if update_in.status in [OrderStatus.CANCELLED, OrderStatus.FAILED, OrderStatus.RETURNED]:
            for item in order.items:
                if item.product_id:
                    InventoryService.release_reservation(db, item.product_id, item.quantity)
        elif update_in.status in [OrderStatus.PICKING, OrderStatus.PACKED, OrderStatus.READY_FOR_DISPATCH, OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED]:
            if old_status == OrderStatus.CREATED or old_status == OrderStatus.CONFIRMED:
                for item in order.items:
                    if item.product_id:
                        InventoryService.commit_reservation(db, item.product_id, item.quantity)

        if order.delivery:
            if update_in.status == OrderStatus.OUT_FOR_DELIVERY:
                order.delivery.status = DeliveryStatus.IN_TRANSIT
            elif update_in.status == OrderStatus.DELIVERED:
                order.delivery.status = DeliveryStatus.DELIVERED
                order.delivery.actual_delivery = datetime.now(timezone.utc)

        db.commit()
        db.refresh(order)
        return order
