from typing import Optional, List
from sqlalchemy.orm import Session

from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_repository import UserRepository
from app.models.notification_model import Notification
from app.schemas.notification_schemas import NotificationCreate


class NotificationService:

    def __init__(self, db: Session):
        self.db = db
        self.notification_repo = NotificationRepository(db)
        self.user_repo = UserRepository(db)

    def create_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        type: str,
        related_id: Optional[int] = None,
    ) -> Notification:
        notification = self.notification_repo.create(
            user_id=user_id,
            title=title,
            message=message,
            type=type,
            related_id=related_id,
            is_read=False,
        )
        return notification

    def get_notification(self, notification_id: int) -> Optional[Notification]:
        return self.notification_repo.get(notification_id)

    def get_user_notifications(self, user_id: int) -> List[Notification]:
        return self.notification_repo.get_by_user(user_id)

    def get_user_unread_notifications(self, user_id: int) -> List[Notification]:
        return self.notification_repo.get_unread_by_user(user_id)

    def get_unread_count(self, user_id: int) -> int:
        return self.notification_repo.get_unread_count(user_id)

    def get_recent_notifications(
        self,
        user_id: int,
        limit: int = 10
    ) -> List[Notification]:
        return self.notification_repo.get_recent_by_user(user_id, limit)

    def mark_as_read(self, notification_id: int) -> bool:
        return self.notification_repo.mark_as_read(notification_id)

    def mark_all_as_read(self, user_id: int) -> int:
        return self.notification_repo.mark_all_as_read(user_id)

    def delete_notification(self, notification_id: int) -> bool:
        return self.notification_repo.delete(notification_id)

    def create_bulk_notifications(
        self,
        user_ids: List[int],
        title: str,
        message: str,
        type: str,
        related_id: Optional[int] = None,
    ) -> int:
        count = 0
        for user_id in user_ids:
            self.create_notification(
                user_id=user_id,
                title=title,
                message=message,
                type=type,
                related_id=related_id,
            )
            count += 1
        return count

    def create_notice_notifications(
        self,
        department_id: int,
        notice_id: int,
        title: str,
        message: str,
    ) -> int:
        students = self.user_repo.get_students_by_department(department_id)
        user_ids = [student.id for student in students]
        
        return self.create_bulk_notifications(
            user_ids=user_ids,
            title=f"New Notice: {title}",
            message=message[:200], 
            type="notice",
            related_id=notice_id,
        )

    def create_assignment_notifications(
        self,
        department_id: int,
        assignment_id: int,
        title: str,
        deadline: str,
    ) -> int:
        students = self.user_repo.get_students_by_department(department_id)
        user_ids = [student.id for student in students]
        
        return self.create_bulk_notifications(
            user_ids=user_ids,
            title=f"New Assignment: {title}",
            message=f"Due: {deadline}",
            type="assignment",
            related_id=assignment_id,
        )