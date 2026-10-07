from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile_schemas import ProfileCreate, ProfileUpdate
from app.models.profile_model import Profile


class ProfileService:
    def __init__(self, db: Session):
        self.db = db
        self.profile_repo = ProfileRepository(db)

    def create_profile(self, user_id: int, data: ProfileCreate) -> Profile:
        return self.profile_repo.create(
            user_id=user_id,
            **data.model_dump(exclude_unset=True),
        )

    def get_profile(self, user_id: int) -> Optional[Profile]:
        return self.profile_repo.get_by_user_id(user_id)

    def update_profile(self, user_id: int, data: ProfileUpdate) -> Optional[Profile]:
        profile = self.profile_repo.get_by_user_id(user_id)
        if not profile:
            return None
        update_data = data.model_dump(exclude_unset=True)
        return self.profile_repo.update(profile.id, **update_data)