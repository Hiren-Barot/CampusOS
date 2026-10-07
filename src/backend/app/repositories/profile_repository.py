from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.profile_model import Profile
from app.repositories.base_repository import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    def __init__(self, db: Session):
        super().__init__(Profile, db)

    def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        stmt = select(Profile).where(Profile.user_id == user_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_enrollment_no(self, enrollment_no: str) -> Optional[Profile]:
        stmt = select(Profile).where(Profile.enrollment_no == enrollment_no)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()