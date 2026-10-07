from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func

from app.models.user_model import User
from app.models.profile_model import Profile
from app.models.notification_model import Notification
from app.models.query_model import Query
from app.models.notice_model import Notice
from app.models.assignment_model import Assignment
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_role(self, role: str) -> List[User]:
        stmt = select(User).where(User.role == role, User.is_active == True)
        return self.db.execute(stmt).scalars().all()

    def get_by_department(self, department_id: int) -> List[User]:
        stmt = select(User).where(
            User.department_id == department_id,
            User.is_active == True,
        )
        return self.db.execute(stmt).scalars().all()

    def get_faculty_by_department(self, department_id: int) -> List[User]:
        stmt = select(User).where(
            User.department_id == department_id,
            User.role.in_(["faculty", "hod"]),
            User.is_active == True,
        )
        return self.db.execute(stmt).scalars().all()

    def get_students_by_department(self, department_id: int) -> List[User]:
        stmt = select(User).where(
            User.department_id == department_id,
            User.role == "student",
            User.is_active == True,
        )
        return self.db.execute(stmt).scalars().all()

    def search_users(self, query: str) -> List[User]:
        stmt = select(User).where(
            User.is_active == True,
            or_(
                User.full_name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%"),
            )
        )
        return self.db.execute(stmt).scalars().all()
    
    def can_hard_delete(self, user_id: int) -> Tuple[bool, str]:
        notice_count = self.db.query(func.count(Notice.id)).filter(
            Notice.faculty_id == user_id
        ).scalar() or 0
        if notice_count > 0:
            return False, f"User has {notice_count} notice(s). Delete those first."

        assignment_count = self.db.query(func.count(Assignment.id)).filter(
            Assignment.faculty_id == user_id
        ).scalar() or 0
        if assignment_count > 0:
            return False, f"User has {assignment_count} assignment(s). Delete those first."

        return True, ""

    def hard_delete(self, user_id: int) -> bool:
        user = self.get(user_id)
        if not user:
            return False

        can_delete, _ = self.can_hard_delete(user_id)
        if not can_delete:
            return False

        try:
            self.db.query(Notification).filter(
                Notification.user_id == user_id
            ).delete(synchronize_session=False)

            self.db.query(Query).filter(
                Query.replied_by_id == user_id
            ).update(
                {"replied_by_id": None},
                synchronize_session=False,
            )

            self.db.query(Query).filter(
                Query.student_id == user_id
            ).delete(synchronize_session=False)

            self.db.query(Profile).filter(
                Profile.user_id == user_id
            ).delete(synchronize_session=False)

            self.db.delete(user)
            self.db.commit()
            return True

        except Exception:
            self.db.rollback()
            raise