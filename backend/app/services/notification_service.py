from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.notification import Notification, NotificationType
from app.schemas.notification import NotificationCreate


class NotificationService:
    @staticmethod
    def get_user_notifications(db: Session, user_id: int, unread_only: bool = False, skip: int = 0, limit: int = 50) -> List[Notification]:
        q = db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            q = q.filter(Notification.is_read == False)
        return q.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_notification(db: Session, notif_in: NotificationCreate) -> Notification:
        notif = Notification(
            user_id=notif_in.user_id,
            title=notif_in.title,
            message=notif_in.message,
            type=notif_in.type,
            metadata_json=notif_in.metadata_json,
            is_read=False
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)
        return notif

    @staticmethod
    def mark_as_read(db: Session, notification_id: int, user_id: int) -> Notification:
        notif = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        if not notif:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        notif.is_read = True
        db.commit()
        db.refresh(notif)
        return notif

    @staticmethod
    def mark_all_as_read(db: Session, user_id: int) -> None:
        db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True})
        db.commit()
