from typing import Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.cart import Cart, CartItem
from app.models.product import Product, ProductStatus
from app.models.inventory import Inventory
from app.schemas.cart import CartResponse, CartItemResponse
from app.schemas.product import ProductResponse


class CartService:
    @staticmethod
    def get_or_create_cart(db: Session, user_id: Optional[int] = None, session_id: Optional[str] = None) -> Cart:
        if not user_id and not session_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either user_id or session_id is required")

        cart = None
        if user_id:
            cart = db.query(Cart).options(
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.farmer),
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.category),
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.inventory)
            ).filter(Cart.user_id == user_id).first()
        elif session_id:
            cart = db.query(Cart).options(
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.farmer),
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.category),
                joinedload(Cart.items).joinedload(CartItem.product).joinedload(Product.inventory)
            ).filter(Cart.session_id == session_id).first()

        if not cart:
            cart = Cart(user_id=user_id, session_id=session_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)

        return cart

    @staticmethod
    def add_item(db: Session, cart_id: int, product_id: int, quantity: float = 1.0) -> Cart:
        product = db.query(Product).options(joinedload(Product.inventory)).filter(Product.id == product_id).first()
        if not product or product.status != ProductStatus.ACTIVE:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not available")

        inv = product.inventory
        if not inv or inv.available_quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {inv.available_quantity if inv else 0} {product.unit} available in stock"
            )

        item = db.query(CartItem).filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id
        ).first()

        if item:
            item.quantity += quantity
            item.unit_price = product.base_price
        else:
            item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.base_price
            )
            db.add(item)

        db.commit()
        return db.query(Cart).filter(Cart.id == cart_id).first()

    @staticmethod
    def update_item_quantity(db: Session, cart_id: int, item_id: int, quantity: float) -> Cart:
        item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

        if quantity <= 0:
            db.delete(item)
        else:
            product = db.query(Product).options(joinedload(Product.inventory)).filter(Product.id == item.product_id).first()
            if product and product.inventory and product.inventory.available_quantity < quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Only {product.inventory.available_quantity} {product.unit} available in stock"
                )
            item.quantity = quantity
            item.unit_price = product.base_price if product else item.unit_price

        db.commit()
        return db.query(Cart).filter(Cart.id == cart_id).first()

    @staticmethod
    def remove_item(db: Session, cart_id: int, item_id: int) -> Cart:
        item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
        if item:
            db.delete(item)
            db.commit()
        return db.query(Cart).filter(Cart.id == cart_id).first()

    @staticmethod
    def clear_cart(db: Session, cart_id: int) -> None:
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
        db.commit()

    @staticmethod
    def format_cart_response(cart: Cart) -> CartResponse:
        item_responses = []
        subtotal = 0.0
        farmer_total = 0.0
        market_total = 0.0
        total_items = 0

        for item in cart.items:
            prod = item.product
            item_subtotal = round(item.quantity * item.unit_price, 2)
            subtotal += item_subtotal
            total_items += int(item.quantity)

            if prod:
                farmer_total += round(item.quantity * prod.farmer_price, 2)
                market_price = prod.market_price or (prod.base_price * 1.25)
                market_total += round(item.quantity * market_price, 2)

            prod_response = ProductResponse.model_validate(prod) if prod else None

            item_responses.append(CartItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item_subtotal,
                product=prod_response,
                created_at=item.created_at,
                updated_at=item.updated_at
            ))

        subtotal = round(subtotal, 2)
        farmer_total = round(farmer_total, 2)
        market_total = round(market_total, 2)
        savings = max(0.0, round(market_total - subtotal, 2))
        delivery_fee = 0.0 if (subtotal >= 299.0 or len(item_responses) == 0) else 35.0
        total_amount = round(subtotal + delivery_fee, 2)

        return CartResponse(
            id=cart.id,
            user_id=cart.user_id,
            session_id=cart.session_id,
            items=item_responses,
            item_count=total_items,
            subtotal=subtotal,
            farmer_total=farmer_total,
            market_total=market_total,
            savings=savings,
            delivery_fee=delivery_fee,
            total_amount=total_amount
        )
