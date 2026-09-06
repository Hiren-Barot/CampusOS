from typing import Optional, List
from sqlalchemy.orm import Session

from app.repositories.notice_repository import NoticeRepository
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import DepartmentRepository
from app.schemas.notice_schemas import NoticeCreate, NoticeUpdate
from app.models.notice_model import Notice
from app.services.notification_service import NotificationService


class NoticeService:

    def __init__(self, db: Session):
        self.db = db
        self.notice_repo = NoticeRepository(db)
        self.user_repo = UserRepository(db)
        self.dept_repo = DepartmentRepository(db)
        self.notification_service = NotificationService(db)

    def create_notice(self, notice_data: NoticeCreate, faculty_id: int) -> Notice:
        notice = self.notice_repo.create(
            **notice_data.model_dump(),
            faculty_id=faculty_id,
        )

        students = self.user_repo.get_students_by_department(notice_data.department_id)
        for student in students:
            self.notification_service.create_notification(
                user_id=student.id,
                title=f"New Notice: {notice_data.title}",
                message=f"{notice_data.content[:100]}...",
                type="notice",
                related_id=notice.id,
            )

        return notice

    def get_notice(self, notice_id: int) -> Optional[Notice]:
        return self.notice_repo.get(notice_id)

    def get_all_notices(self, skip: int = 0, limit: int = 100) -> List[Notice]:
        return self.notice_repo.get_all(skip=skip, limit=limit)

    def get_notices_by_department(self, department_id: int) -> List[Notice]:
        return self.notice_repo.get_by_department(department_id)

    def get_notices_by_faculty(self, faculty_id: int) -> List[Notice]:
        return self.notice_repo.get_by_faculty(faculty_id)

    def get_published_notices(self) -> List[Notice]:
        return self.notice_repo.get_published()

    def get_draft_notices(self, faculty_id: int) -> List[Notice]:
        return self.notice_repo.get_drafts(faculty_id)

    def get_recent_notices(self, limit: int = 10) -> List[Notice]:
        return self.notice_repo.get_recent(limit)

    def update_notice(self, notice_id: int, notice_data: NoticeUpdate) -> Optional[Notice]:
        update_data = notice_data.model_dump(exclude_unset=True)
        return self.notice_repo.update(notice_id, **update_data)

    def delete_notice(self, notice_id: int) -> bool:
        return self.notice_repo.delete(notice_id)

    def publish_notice(self, notice_id: int) -> Optional[Notice]:
        return self.notice_repo.update(notice_id, is_published=True)

    def unpublish_notice(self, notice_id: int) -> Optional[Notice]:
        return self.notice_repo.update(notice_id, is_published=False)

    def search_notices(self, query: str) -> List[Notice]:
        return self.notice_repo.search_notices(query)

    def get_department_notices_with_author(self, department_id: int) -> List[dict]:
        notices = self.notice_repo.get_by_department(department_id)
        result = []

        for notice in notices:
            faculty = self.user_repo.get(notice.faculty_id)
            result.append({
                "id": notice.id,
                "title": notice.title,
                "content": notice.content,
                "is_published": notice.is_published,
                "created_at": notice.created_at,
                "updated_at": notice.updated_at,
                "faculty_id": notice.faculty_id,
                "faculty_name": faculty.full_name if faculty else "Unknown",
            })

        return result

    def can_edit_notice(self, notice_id: int, user_id: int) -> bool:
        notice = self.notice_repo.get(notice_id)
        if not notice:
            return False

        user = self.user_repo.get(user_id)
        if not user:
            return False

        if user.role == "admin":
            return True

        if user.role == "principal":
            return True

        if user.role == "hod" and user.department_id == notice.department_id:
            return True

        if user.role == "faculty" and user.id == notice.faculty_id:
            return True

        return False

    def can_delete_notice(self, notice_id: int, user_id: int) -> bool:
        return self.can_edit_notice(notice_id, user_id)