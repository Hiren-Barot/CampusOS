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

    def _enrich_notice(self, notice: Notice) -> dict:
        faculty = self.user_repo.get(notice.faculty_id)
        return {
            "id": notice.id,
            "title": notice.title,
            "content": notice.content,
            "department_id": notice.department_id,
            "faculty_id": notice.faculty_id,
            "faculty_name": faculty.full_name if faculty else "Unknown",
            "is_published": notice.is_published,
            "created_at": notice.created_at,
            "updated_at": notice.updated_at,
        }
    
    def create_notice(self, notice_data: NoticeCreate, faculty_id: int) -> dict:
        creator = self.user_repo.get(faculty_id)
        if not creator:
            raise ValueError("Creator not found")

        dept_id = notice_data.department_id

        if creator.role in ["admin", "principal"]:
            pass
        else:
            if not creator.department_id:
                raise ValueError("You have no department assigned")
            dept_id = creator.department_id

        notice = self.notice_repo.create(
            title=notice_data.title,
            content=notice_data.content,
            department_id=dept_id,
            is_published=notice_data.is_published,
            faculty_id=faculty_id,
        )

        self._notify_students(notice, dept_id)

        return self._enrich_notice(notice)

    def _notify_students(self, notice: Notice, dept_id: Optional[int]):
        if dept_id:
            students = self.user_repo.get_students_by_department(dept_id)
        else:
            students = self.user_repo.get_by_role("student")

        for student in students:
            self.notification_service.create_notification(
                user_id=student.id,
                title=f"New Notice: {notice.title}",
                message=notice.content[:100] + ("..." if len(notice.content) > 100 else ""),
                type="notice",
                related_id=notice.id,
            )

    def get_notice(self, notice_id: int) -> Optional[dict]:
        notice = self.notice_repo.get(notice_id)
        return self._enrich_notice(notice) if notice else None

    def get_all_notices(self, skip: int = 0, limit: int = 100) -> List[dict]:
        notices = self.notice_repo.get_all(skip=skip, limit=limit)
        return [self._enrich_notice(n) for n in notices]

    def get_notices_by_department(self, department_id: int) -> List[dict]:
        notices = self.notice_repo.get_by_department(department_id)
        return [self._enrich_notice(n) for n in notices]

    def get_notices_by_faculty(self, faculty_id: int) -> List[dict]:
        notices = self.notice_repo.get_by_faculty(faculty_id)
        return [self._enrich_notice(n) for n in notices]

    def get_published_notices(self) -> List[dict]:
        notices = self.notice_repo.get_published()
        return [self._enrich_notice(n) for n in notices]

    def get_draft_notices(self, faculty_id: int) -> List[dict]:
        notices = self.notice_repo.get_drafts(faculty_id)
        return [self._enrich_notice(n) for n in notices]

    def get_recent_notices(self, limit: int = 10) -> List[dict]:
        notices = self.notice_repo.get_recent(limit)
        return [self._enrich_notice(n) for n in notices]

    def update_notice(self, notice_id: int, notice_data: NoticeUpdate) -> Optional[dict]:
        update_data = notice_data.model_dump(exclude_unset=True)
        notice = self.notice_repo.update(notice_id, **update_data)
        return self._enrich_notice(notice) if notice else None

    def publish_notice(self, notice_id: int) -> Optional[dict]:
        notice = self.notice_repo.update(notice_id, is_published=True)
        return self._enrich_notice(notice) if notice else None

    def unpublish_notice(self, notice_id: int) -> Optional[dict]:
        notice = self.notice_repo.update(notice_id, is_published=False)
        return self._enrich_notice(notice) if notice else None

    def delete_notice(self, notice_id: int) -> bool:
        return self.notice_repo.delete(notice_id)

    def search_notices(self, query: str) -> List[dict]:
        notices = self.notice_repo.search_notices(query)
        return [self._enrich_notice(n) for n in notices]

    def can_edit_notice(self, notice_id: int, user_id: int) -> bool:
        notice = self.notice_repo.get(notice_id)
        if not notice:
            return False
        return notice.faculty_id == user_id

    def can_delete_notice(self, notice_id: int, user_id: int) -> bool:
        return self.can_edit_notice(notice_id, user_id)