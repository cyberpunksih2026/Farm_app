from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductDetailResponse
from app.schemas.common import APIResponse
from app.services.product_service import ProductService
from app.api.v1.deps import require_admin

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=APIResponse[List[ProductResponse]])
def list_products(
    query: Optional[str] = Query(None, description="Search by crop name or keyword"),
    category: Optional[str] = Query(None, description="Filter by category slug (e.g. vegetables, fruits)"),
    organic: Optional[bool] = Query(None, description="Filter organic certified produce"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    products = ProductService.get_all(
        db,
        query=query,
        category_slug=category,
        is_organic=organic,
        skip=skip,
        limit=limit
    )
    return APIResponse(
        success=True,
        message="Products retrieved successfully",
        data=[ProductResponse.model_validate(p) for p in products]
    )


@router.get("/{product_id}", response_model=APIResponse[ProductDetailResponse])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get_by_id(db, product_id)
    return APIResponse(
        success=True,
        message="Product details retrieved",
        data=ProductDetailResponse.model_validate(product)
    )


@router.get("/slug/{slug}", response_model=APIResponse[ProductDetailResponse])
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    product = ProductService.get_by_slug(db, slug)
    return APIResponse(
        success=True,
        message="Product details retrieved",
        data=ProductDetailResponse.model_validate(product)
    )


@router.post("", response_model=APIResponse[ProductResponse], status_code=status.HTTP_201_CREATED)
def create_product(
    prod_in: ProductCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    product = ProductService.create(db, prod_in)
    return APIResponse(
        success=True,
        message="Product created successfully with linked inventory",
        data=ProductResponse.model_validate(product)
    )


@router.put("/{product_id}", response_model=APIResponse[ProductResponse])
def update_product(
    product_id: int,
    prod_update: ProductUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    product = ProductService.update(db, product_id, prod_update)
    return APIResponse(
        success=True,
        message="Product updated successfully",
        data=ProductResponse.model_validate(product)
    )


@router.delete("/{product_id}", response_model=APIResponse[bool])
def delete_product(
    product_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    ProductService.delete(db, product_id)
    return APIResponse(success=True, message="Product deactivated successfully", data=True)
