from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.product import Product, ProductStatus
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)

    def get_with_details(self, db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).options(
            joinedload(Product.farmer),
            joinedload(Product.category),
            joinedload(Product.inventory)
        ).filter(Product.id == product_id).first()

    def get_by_slug(self, db: Session, slug: str) -> Optional[Product]:
        return db.query(Product).options(
            joinedload(Product.farmer),
            joinedload(Product.category),
            joinedload(Product.inventory)
        ).filter(Product.slug == slug).first()

    def search_active(
        self,
        db: Session,
        query: Optional[str] = None,
        category_id: Optional[int] = None,
        category_slug: Optional[str] = None,
        is_organic: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Product]:
        q = db.query(Product).options(
            joinedload(Product.farmer),
            joinedload(Product.category),
            joinedload(Product.inventory)
        ).filter(Product.status == ProductStatus.ACTIVE)

        if category_id:
            q = q.filter(Product.category_id == category_id)
        if category_slug and category_slug != "all":
            q = q.join(Product.category).filter(Product.category.has(slug=category_slug))
        if is_organic is not None:
            q = q.filter(Product.is_organic == is_organic)
        if query:
            search_pattern = f"%{query.strip()}%"
            q = q.filter(
                (Product.name.ilike(search_pattern)) |
                (Product.description.ilike(search_pattern))
            )

        return q.offset(skip).limit(limit).all()


product_repo = ProductRepository()
