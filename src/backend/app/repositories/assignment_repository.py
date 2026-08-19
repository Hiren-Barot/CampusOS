from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, desc, asc
from datetime import datetime

from src.backend.app.models.assignment_model import Assignment
from src.backend.app.repositories.base_repository import BaseRepository


class AssignmentRepository(BaseRepository[Assignment]):

    def __init__(self, db: Session):
        super().__init__(Assignment, db)

    def get_by_department(self, department_id: int) -> List[Assignment]:
        """Get all assignments in a specific department."""
        stmt = select(Assignment).where(
            Assignment.department_id == department_id
        ).order_by(asc(Assignment.deadline))
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_faculty(self, faculty_id: int) -> List[Assignment]:
        """Get all assignments created by a specific faculty member."""
        stmt = select(Assignment).where(
            Assignment.faculty_id == faculty_id
        ).order_by(desc(Assignment.created_at))
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_upcoming(
        self,
        department_id: Optional[int] = None
    ) -> List[Assignment]:
        """Get upcoming assignments (deadline >= now)."""
        stmt = select(Assignment).where(
            Assignment.deadline >= datetime.now()
        )
        
        if department_id:
            stmt = stmt.where(Assignment.department_id == department_id)
        
        stmt = stmt.order_by(asc(Assignment.deadline))
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_expired(
        self,
        department_id: Optional[int] = None
    ) -> List[Assignment]:
        """Get expired assignments (deadline < now)."""
        stmt = select(Assignment).where(
            Assignment.deadline < datetime.now()
        )
        
        if department_id:
            stmt = stmt.where(Assignment.department_id == department_id)
        
        stmt = stmt.order_by(desc(Assignment.deadline))
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_recent(self, limit: int = 10) -> List[Assignment]:
        """Get most recent assignments."""
        stmt = select(Assignment).order_by(
            desc(Assignment.created_at)
        ).limit(limit)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def search_assignments(self, query: str) -> List[Assignment]:
        """Search assignments by title or description."""
        stmt = select(Assignment).where(
            Assignment.title.ilike(f"%{query}%") |
            Assignment.description.ilike(f"%{query}%")
        ).order_by(asc(Assignment.deadline))
        result = self.db.execute(stmt)
        return result.scalars().all()