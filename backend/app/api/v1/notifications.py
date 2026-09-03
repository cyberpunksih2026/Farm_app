from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.notification import NotificationResponse, NotificationCreate
from app.schemas.common import APIResponse
from app.services.notification_service import NotificationService
from app.api.v1.deps import get_current_user, require_admin

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=APIResponse[List[NotificationResponse]])
def get_my_notifications(
    unread_only: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notifs = NotificationService.get_user_notifications(
        db,
        user_id=current_user.id,
        unread_only=unread_only,
        skip=skip,
        limit=limit
    )
    return APIResponse(
        success=True,
        message="Notifications retrieved",
        data=[NotificationResponse.model_validate(n) for n in notifs]
    )


@router.post("/{notification_id}/read", response_model=APIResponse[NotificationResponse])
def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notif = NotificationService.mark_as_read(db, notification_id, current_user.id)
    return APIResponse(
        success=True,
        message="Notification marked as read",
        data=NotificationResponse.model_validate(notif)
    )


@router.post("/read-all", response_model=APIResponse[bool])
def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    NotificationService.mark_all_as_read(db, current_user.id)
    return APIResponse(success=True, message="All notifications marked as read", data=True)


@router.post("/broadcast", response_model=APIResponse[NotificationResponse], status_code=status.HTTP_201_CREATED)
def broadcast_notification(
    notif_in: NotificationCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    notif = NotificationService.create_notification(db, notif_in)
    return APIResponse(
        success=True,
        message="Notification dispatched",
        data=NotificationResponse.model_validate(notif)
    )
