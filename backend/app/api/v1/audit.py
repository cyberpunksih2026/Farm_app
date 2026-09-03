from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.audit import AuditLogResponse
from app.schemas.common import APIResponse, PaginatedResponse
from app.services.audit_service import AuditService
from app.api.v1.deps import require_admin

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs (Admin)"])


@router.get("", response_model=APIResponse[PaginatedResponse[AuditLogResponse]])
def list_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    entity_type: Optional[str] = None,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    items, total = AuditService.get_audit_logs(
        db,
        skip=(page - 1) * page_size,
        limit=page_size,
        action=action,
        user_id=user_id,
        entity_type=entity_type
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return APIResponse(
        success=True,
        message="Audit logs retrieved successfully",
        data=PaginatedResponse(
            items=[AuditLogResponse.model_validate(log) for log in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    )
