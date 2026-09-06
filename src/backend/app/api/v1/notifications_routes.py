from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.notification_schemas import (
    NotificationResponse,
    NotificationCount,
)
from app.services.notification_service import NotificationService
from app.models.user_model import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=List[NotificationResponse])
async def get_my_notifications(
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification_service = NotificationService(db)
    notifications = notification_service.get_recent_notifications(
        user_id=current_user.id,
        limit=limit,
    )
    return notifications


@router.get("/unread", response_model=List[NotificationResponse])
async def get_unread_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification_service = NotificationService(db)
    notifications = notification_service.get_user_unread_notifications(
        user_id=current_user.id,
    )
    return notifications


@router.get("/unread/count", response_model=NotificationCount)
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification_service = NotificationService(db)
    count = notification_service.get_unread_count(user_id=current_user.id)
    return NotificationCount(count=count)


@router.patch("/read-all")
async def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification_service = NotificationService(db)
    count = notification_service.mark_all_as_read(user_id=current_user.id)
    
    return {"message": f"{count} notifications marked as read"}

@router.patch("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification_service = NotificationService(db)
    notification = notification_service.get_notification(notification_id)
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only mark your own notifications",
        )
    
    success = notification_service.mark_as_read(notification_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark notification as read",
        )
    
    return {"message": "Notification marked as read"}



@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification_service = NotificationService(db)
    notification = notification_service.get_notification(notification_id)
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own notifications",
        )
    
    success = notification_service.delete_notification(notification_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete notification",
        )
    
    return {"message": "Notification deleted successfully"}