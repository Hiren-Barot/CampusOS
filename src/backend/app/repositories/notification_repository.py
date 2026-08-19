from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, desc, func

from src.backend.app.models.notification_model import Notification
from src.backend.app.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    
    def __init__(self, db: Session):
        super().__init__(Notification, db)

    def get_by_user(self, user_id: int) -> List[Notification]:
        """Get all notifications for a specific user."""
        stmt = select(Notification).where(
            Notification.user_id == user_id
        ).order_by(desc(Notification.created_at))
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_unread_by_user(self, user_id: int) -> List[Notification]:
        """Get all unread notifications for a specific user."""
        stmt = select(Notification).where(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).order_by(desc(Notification.created_at))
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications for a user."""
        stmt = select(func.count()).select_from(Notification).where(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        result = self.db.execute(stmt)
        return result.scalar() or 0

    def mark_as_read(self, notification_id: int) -> bool:
        """Mark a specific notification as read."""
        notification = self.get(notification_id)
        if not notification:
            return False
        notification.is_read = True
        self.db.commit()
        return True

    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications for a user as read."""
        stmt = select(Notification).where(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        result = self.db.execute(stmt)
        notifications = result.scalars().all()
        
        count = 0
        for notification in notifications:
            notification.is_read = True
            count += 1
        
        self.db.commit()
        return count

    def get_recent_by_user(self, user_id: int, limit: int = 10) -> List[Notification]:
        """Get most recent notifications for a user."""
        stmt = select(Notification).where(
            Notification.user_id == user_id
        ).order_by(desc(Notification.created_at)).limit(limit)
        result = self.db.execute(stmt)
        return result.scalars().all()