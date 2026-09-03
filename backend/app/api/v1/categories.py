from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.common import APIResponse
from app.api.v1.deps import require_admin

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=APIResponse[List[CategoryResponse]])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).filter(Category.is_active == True).order_by(Category.display_order.asc()).all()
    return APIResponse(
        success=True,
        message="Categories retrieved successfully",
        data=[CategoryResponse.model_validate(c) for c in categories]
    )


@router.get("/{category_id}", response_model=APIResponse[CategoryResponse])
def get_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return APIResponse(
        success=True,
        message="Category details retrieved",
        data=CategoryResponse.model_validate(cat)
    )


@router.post("", response_model=APIResponse[CategoryResponse], status_code=status.HTTP_201_CREATED)
def create_category(
    cat_in: CategoryCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    existing = db.query(Category).filter(Category.slug == cat_in.slug).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category slug already exists")
    
    cat = Category(**cat_in.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return APIResponse(
        success=True,
        message="Category created successfully",
        data=CategoryResponse.model_validate(cat)
    )


@router.put("/{category_id}", response_model=APIResponse[CategoryResponse])
def update_category(
    category_id: int,
    cat_in: CategoryUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    for k, v in cat_in.model_dump(exclude_unset=True).items():
        setattr(cat, k, v)
    db.commit()
    db.refresh(cat)
    return APIResponse(
        success=True,
        message="Category updated successfully",
        data=CategoryResponse.model_validate(cat)
    )
