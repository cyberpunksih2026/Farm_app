from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.cart import CartResponse, CartItemAddRequest, CartItemUpdateRequest
from app.schemas.common import APIResponse
from app.services.cart_service import CartService
from app.api.v1.deps import get_optional_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", response_model=APIResponse[CartResponse])
def get_cart(
    session_id: Optional[str] = Query(None, description="Guest session ID if unauthenticated"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id if current_user else None
    cart = CartService.get_or_create_cart(db, user_id=user_id, session_id=session_id)
    summary = CartService.format_cart_response(cart)
    return APIResponse(
        success=True,
        message="Cart retrieved successfully",
        data=summary
    )


@router.post("/items", response_model=APIResponse[CartResponse], status_code=status.HTTP_201_CREATED)
def add_cart_item(
    item_in: CartItemAddRequest,
    session_id: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id if current_user else None
    cart = CartService.get_or_create_cart(db, user_id=user_id, session_id=session_id)
    cart = CartService.add_item(db, cart.id, item_in.product_id, item_in.quantity)
    summary = CartService.format_cart_response(cart)
    return APIResponse(
        success=True,
        message="Item added to cart",
        data=summary
    )


@router.put("/items/{item_id}", response_model=APIResponse[CartResponse])
def update_cart_item(
    item_id: int,
    item_update: CartItemUpdateRequest,
    session_id: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id if current_user else None
    cart = CartService.get_or_create_cart(db, user_id=user_id, session_id=session_id)
    cart = CartService.update_item_quantity(db, cart.id, item_id, item_update.quantity)
    summary = CartService.format_cart_response(cart)
    return APIResponse(
        success=True,
        message="Cart item updated",
        data=summary
    )


@router.delete("/items/{item_id}", response_model=APIResponse[CartResponse])
def remove_cart_item(
    item_id: int,
    session_id: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id if current_user else None
    cart = CartService.get_or_create_cart(db, user_id=user_id, session_id=session_id)
    cart = CartService.remove_item(db, cart.id, item_id)
    summary = CartService.format_cart_response(cart)
    return APIResponse(
        success=True,
        message="Item removed from cart",
        data=summary
    )


@router.delete("", response_model=APIResponse[bool])
def clear_cart(
    session_id: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id if current_user else None
    cart = CartService.get_or_create_cart(db, user_id=user_id, session_id=session_id)
    CartService.clear_cart(db, cart.id)
    return APIResponse(success=True, message="Cart cleared successfully", data=True)
