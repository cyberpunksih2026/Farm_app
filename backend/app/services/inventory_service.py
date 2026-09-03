from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.inventory import Inventory
from app.models.product import Product, ProductStatus
from app.schemas.inventory import InventoryUpdate


class InventoryService:
    @staticmethod
    def get_by_product_id(db: Session, product_id: int) -> Inventory:
        inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
        if not inv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory record not found")
        return inv

    @staticmethod
    def update(db: Session, product_id: int, update_data: InventoryUpdate) -> Inventory:
        inv = InventoryService.get_by_product_id(db, product_id)
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(inv, field, value)
        db.commit()
        db.refresh(inv)
        return inv

    @staticmethod
    def restock(db: Session, product_id: int, quantity: float) -> Inventory:
        if quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Restock quantity must be positive")
        inv = InventoryService.get_by_product_id(db, product_id)
        inv.stock_quantity += quantity
        inv.last_restocked_at = datetime.now(timezone.utc)
        
        product = db.query(Product).filter(Product.id == product_id).first()
        if product and product.status == ProductStatus.OUT_OF_STOCK and inv.available_quantity > 0:
            product.status = ProductStatus.ACTIVE

        db.commit()
        db.refresh(inv)
        return inv

    @staticmethod
    def reserve_stock(db: Session, product_id: int, quantity: float) -> bool:
        inv = db.query(Inventory).filter(Inventory.product_id == product_id).with_for_update().first()
        if not inv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Inventory not found for product {product_id}")
        
        if inv.available_quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient inventory for product {product_id}. Available: {inv.available_quantity} {inv.unit}, Requested: {quantity} {inv.unit}"
            )

        inv.reserved_quantity += quantity
        return True

    @staticmethod
    def release_reservation(db: Session, product_id: int, quantity: float) -> None:
        inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
        if inv:
            inv.reserved_quantity = max(0.0, inv.reserved_quantity - quantity)

    @staticmethod
    def commit_reservation(db: Session, product_id: int, quantity: float) -> None:
        inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
        if inv:
            inv.stock_quantity = max(0.0, inv.stock_quantity - quantity)
            inv.reserved_quantity = max(0.0, inv.reserved_quantity - quantity)
            
            product = db.query(Product).filter(Product.id == product_id).first()
            if product and inv.available_quantity <= 0:
                product.status = ProductStatus.OUT_OF_STOCK
