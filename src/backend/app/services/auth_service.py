from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash, create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schemas import UserLogin, UserRegister
from app.models.user_model import User


class AuthService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def authenticate_user(self, login_data: UserLogin) -> Optional[User]:
        user = self.user_repo.get_by_email(login_data.email)
        if not user:
            return None

        if not verify_password(login_data.password, user.hashed_password):
            return None

        return user

    def register_user(self, register_data: UserRegister) -> Optional[User]:
        existing_user = self.user_repo.get_by_email(register_data.email)
        if existing_user:
            return None

        hashed_password = get_password_hash(register_data.password)
        user = self.user_repo.create(
            email=register_data.email,
            hashed_password=hashed_password,
            full_name=register_data.full_name,
            role="student", 
            is_active=True,
            must_change_password=False,
        )
        return user

    def create_access_token(self, user: User) -> str:
        token_data = {"sub": str(user.id), "role": user.role}
        return create_access_token(token_data)