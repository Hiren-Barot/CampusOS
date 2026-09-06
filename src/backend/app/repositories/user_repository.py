from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user_model import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_role(self, role: str) -> List[User]:
        stmt = select(User).where(User.role == role)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_department(self, department_id: int) -> List[User]:
        stmt = select(User).where(User.department_id == department_id)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_faculty_by_department(self, department_id: int) -> List[User]:
        stmt = select(User).where(
            User.department_id == department_id,
            User.role.in_(["faculty", "hod"])
        )
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_students_by_department(self, department_id: int) -> List[User]:
        stmt = select(User).where(
            User.department_id == department_id,
            User.role == "student"
        )
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_active_users(self) -> List[User]:
        stmt = select(User).where(User.is_active == True)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def search_users(self, query: str) -> List[User]:
        stmt = select(User).where(
            User.full_name.ilike(f"%{query}%") |
            User.email.ilike(f"%{query}%")
        )
        result = self.db.execute(stmt)
        return result.scalars().all()