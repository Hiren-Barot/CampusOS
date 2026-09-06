from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.department_model import Department
from app.repositories.base_repository import BaseRepository


class DepartmentRepository(BaseRepository[Department]):

    def __init__(self, db: Session):
        super().__init__(Department, db)

    def get_by_code(self, code: str) -> Optional[Department]:
        stmt = select(Department).where(Department.code == code)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_name(self, name: str) -> Optional[Department]:
        stmt = select(Department).where(Department.name == name)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_with_hod(self, department_id: int) -> Optional[Department]:
        stmt = select(Department).where(Department.id == department_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_all_with_hod(self) -> List[Department]:
        stmt = select(Department)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def search_departments(self, query: str) -> List[Department]:
        stmt = select(Department).where(
            Department.name.ilike(f"%{query}%") |
            Department.code.ilike(f"%{query}%")
        )
        result = self.db.execute(stmt)
        return result.scalars().all()