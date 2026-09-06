from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.inventory import InventoryUpdate, InventoryResponse, RestockRequest
from app.schemas.common import APIResponse
from app.services.inventory_service import InventoryService
from app.api.v1.deps import require_employee, require_admin

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/product/{product_id}", response_model=APIResponse[InventoryResponse])
def get_product_inventory(
    product_id: int,
    db: Session = Depends(get_db)
):
    inv = InventoryService.get_by_product_id(db, product_id)
    return APIResponse(
        success=True,
        message="Inventory status retrieved",
        data=InventoryResponse.model_validate(inv)
    )


@router.put("/product/{product_id}", response_model=APIResponse[InventoryResponse])
def update_inventory(
    product_id: int,
    update_in: InventoryUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    inv = InventoryService.update(db, product_id, update_in)
    return APIResponse(
        success=True,
        message="Inventory updated successfully",
        data=InventoryResponse.model_validate(inv)
    )


@router.post("/product/{product_id}/restock", response_model=APIResponse[InventoryResponse])
def restock_inventory(
    product_id: int,
    restock_in: RestockRequest,
    user: User = Depends(require_employee),
    db: Session = Depends(get_db)
):
    inv = InventoryService.restock(db, product_id, restock_in.quantity)
    return APIResponse(
        success=True,
        message=f"Added {restock_in.quantity} {inv.unit} to stock",
        data=InventoryResponse.model_validate(inv)
    )
