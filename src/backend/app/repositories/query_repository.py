from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.models.query_model import Query
from app.repositories.base_repository import BaseRepository


class QueryRepository(BaseRepository[Query]):

    def __init__(self, db: Session):
        super().__init__(Query, db)

    def get_by_student(self, student_id: int) -> List[Query]:
        stmt = select(Query).where(
            Query.student_id == student_id
        ).order_by(desc(Query.created_at))
        return self.db.execute(stmt).scalars().all()

    def get_by_department(self, department_id: int) -> List[Query]:
        stmt = select(Query).where(
            Query.department_id == department_id
        ).order_by(desc(Query.created_at))
        return self.db.execute(stmt).scalars().all()

    def get_all_ordered(self, skip: int = 0, limit: int = 200) -> List[Query]:
        stmt = select(Query).order_by(
            desc(Query.created_at)
        ).offset(skip).limit(limit)
        return self.db.execute(stmt).scalars().all()

    def get_open_by_department(self, department_id: int) -> List[Query]:
        stmt = select(Query).where(
            Query.department_id == department_id,
            Query.status == "open",
        ).order_by(desc(Query.created_at))
        return self.db.execute(stmt).scalars().all()