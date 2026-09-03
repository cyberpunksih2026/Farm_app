from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.product import Product, ProductStatus
from app.models.inventory import Inventory
from app.models.farmer import Farmer
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product_repo import product_repo


class ProductService:
    @staticmethod
    def get_all(
        db: Session,
        query: Optional[str] = None,
        category_slug: Optional[str] = None,
        is_organic: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Product]:
        return product_repo.search_active(
            db,
            query=query,
            category_slug=category_slug,
            is_organic=is_organic,
            skip=skip,
            limit=limit
        )

    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Product:
        product = product_repo.get_with_details(db, product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Product:
        product = product_repo.get_by_slug(db, slug)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    @staticmethod
    def create(db: Session, product_in: ProductCreate) -> Product:
        farmer = db.query(Farmer).filter(Farmer.id == product_in.farmer_id).first()
        if not farmer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")

        category = db.query(Category).filter(Category.id == product_in.category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        existing = db.query(Product).filter(Product.slug == product_in.slug).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product slug already exists")

        now = datetime.now(timezone.utc)
        product_dict = product_in.model_dump(exclude={"initial_stock"})
        product = Product(**product_dict)
        db.add(product)
        db.flush()

        inventory = Inventory(
            product_id=product.id,
            stock_quantity=product_in.initial_stock or 0.0,
            reserved_quantity=0.0,
            unit=product.unit,
            last_restocked_at=now if product_in.initial_stock else None
        )
        db.add(inventory)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update(db: Session, product_id: int, update_data: ProductUpdate) -> Product:
        product = ProductService.get_by_id(db, product_id)
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, product_id: int) -> None:
        product = ProductService.get_by_id(db, product_id)
        product.status = ProductStatus.INACTIVE
        db.commit()
