from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.logistics import BuyerRequest, LogisticsResult
from app.schemas.common import APIResponse
from app.services.logistics_service import LogisticsService

router = APIRouter(prefix="/logistics", tags=["Logistics & Supply Matching"])


@router.post("/match", response_model=APIResponse[LogisticsResult])
def match_buyer_order(
    buyer: BuyerRequest,
    db: Session = Depends(get_db)
):
    try:
        result = LogisticsService.match_and_allocate_order(db, buyer)
        return APIResponse(
            success=True,
            message=f"Logistics allocation computed: status={result.status}",
            data=result
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
