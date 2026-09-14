from typing import Optional, List, Tuple
from sqlalchemy.orm import Session

from app.core.security.hashing import get_password_hash
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import DepartmentRepository
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.models.user_model import User
from app.utils.password_generator import generate_temp_password


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.dept_repo = DepartmentRepository(db)

    def _enrich_user(self, user: User) -> dict:
        dept_name = None
        if user.department_id:
            dept = self.dept_repo.get(user.department_id)
            if dept:
                dept_name = dept.name

        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "department_id": user.department_id,
            "department_name": dept_name,
            "is_active": user.is_active,
            "must_change_password": user.must_change_password,
            "phone": user.phone,
            "gender": user.gender,
            "date_of_birth": str(user.date_of_birth) if user.date_of_birth else None,
            "profile_picture": user.profile_picture,
            "created_at": user.created_at,
        }

    def create_user(self, user_data: UserCreate) -> Tuple[Optional[User], Optional[str]]:
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

    def get_user_response(self, user_id: int) -> Optional[dict]:
        user = self.user_repo.get(user_id)
        if not user:
            return None
        return self._enrich_user(user)

    def get_all_users(self, skip: int = 0, limit: int = 100, **filters) -> List[dict]:
        if "is_active" not in filters:
            filters["is_active"] = True
        users = self.user_repo.get_all(skip=skip, limit=limit, **filters)
        return [self._enrich_user(u) for u in users]

    def get_users_by_role(self, role: str) -> List[dict]:
        users = self.user_repo.get_by_role(role)
        return [self._enrich_user(u) for u in users]

    def get_users_by_department(self, department_id: int) -> List[dict]:
        users = self.user_repo.get_by_department(department_id)
        return [self._enrich_user(u) for u in users]

    def get_faculty_by_department(self, department_id: int) -> List[dict]:
        users = self.user_repo.get_faculty_by_department(department_id)
        return [self._enrich_user(u) for u in users]

    def get_students_by_department(self, department_id: int) -> List[dict]:
        users = self.user_repo.get_students_by_department(department_id)
        return [self._enrich_user(u) for u in users]

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        update_data = user_data.model_dump(exclude_unset=True)
        return self.user_repo.update(user_id, **update_data)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repo.update(user_id, is_active=False) is not None

    def hard_delete_user(self, user_id: int) -> bool:
        return self.user_repo.delete(user_id)

    def search_users(self, query: str) -> List[dict]:
        users = self.user_repo.search_users(query)
        return [self._enrich_user(u) for u in users]

    def change_password(self, user_id: int, new_password: str) -> bool:
        hashed_password = get_password_hash(new_password)
        user = self.user_repo.update(user_id, hashed_password=hashed_password)
        if user:
            self.user_repo.update(user_id, must_change_password=False)
            return True
        return False