from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.models.notice_model import Notice
from app.repositories.base_repository import BaseRepository


class NoticeRepository(BaseRepository[Notice]):

    def __init__(self, db: Session):
        super().__init__(Notice, db)

    def get_by_department(self, department_id: int) -> List[Notice]:
        stmt = select(Notice).where(
            Notice.department_id == department_id,
            Notice.is_published == True
        ).order_by(desc(Notice.created_at))
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_faculty(self, faculty_id: int) -> List[Notice]:
        stmt = select(Notice).where(
            Notice.faculty_id == faculty_id
        ).order_by(desc(Notice.created_at))
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_published(self) -> List[Notice]:
        stmt = select(Notice).where(
            Notice.is_published == True
        ).order_by(desc(Notice.created_at))
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_drafts(self, faculty_id: int) -> List[Notice]:
        stmt = select(Notice).where(
            Notice.faculty_id == faculty_id,
            Notice.is_published == False
        ).order_by(desc(Notice.created_at))
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_recent(self, limit: int = 10) -> List[Notice]:
        stmt = select(Notice).where(
            Notice.is_published == True
        ).order_by(desc(Notice.created_at)).limit(limit)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def search_notices(self, query: str) -> List[Notice]:
        stmt = select(Notice).where(
            Notice.is_published == True,
            (Notice.title.ilike(f"%{query}%") |
             Notice.content.ilike(f"%{query}%"))
        ).order_by(desc(Notice.created_at))
        result = self.db.execute(stmt)
        return result.scalars().all()
