from typing import Optional, List
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.models.user_model import User
from app.utils.password_generator import generate_temp_password


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> tuple[Optional[User], Optional[str]]:
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            return None, None

        temp_password = generate_temp_password()
        hashed_password = get_password_hash(temp_password)

        user = self.user_repo.create(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role,
            department_id=user_data.department_id,
            is_active=True,
            must_change_password=True,
        )
        return user, temp_password

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_by_email(email)

    def get_all_users(
        self,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[User]:
        return self.user_repo.get_all(skip=skip, limit=limit, **filters)

    def get_users_by_role(self, role: str) -> List[User]:
        return self.user_repo.get_by_role(role)

    def get_users_by_department(self, department_id: int) -> List[User]:
        return self.user_repo.get_by_department(department_id)

    def get_faculty_by_department(self, department_id: int) -> List[User]:
        return self.user_repo.get_faculty_by_department(department_id)

    def get_students_by_department(self, department_id: int) -> List[User]:
        return self.user_repo.get_students_by_department(department_id)

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        update_data = user_data.model_dump(exclude_unset=True)
        return self.user_repo.update(user_id, **update_data)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repo.update(user_id, is_active=False) is not None

    def hard_delete_user(self, user_id: int) -> bool:
        return self.user_repo.delete(user_id)

    def search_users(self, query: str) -> List[User]:
        return self.user_repo.search_users(query)

    def change_password(self, user_id: int, new_password: str) -> bool:
        hashed_password = get_password_hash(new_password)
        user = self.user_repo.update(user_id, hashed_password=hashed_password)
        if user:
            self.user_repo.update(user_id, must_change_password=False)
            return True
        return False