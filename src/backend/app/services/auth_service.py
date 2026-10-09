import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash, create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schemas import UserLogin, UserRegister
from app.models.user_model import User


RESET_TOKEN_EXPIRE_MINUTES = 30


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

    def create_password_reset_token(self, email: str) -> Optional[tuple[User, str]]:
        user = self.user_repo.get_by_email(email)
        if not user:
            return None

        plain_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(plain_token.encode()).hexdigest()

        user.reset_token_hash = token_hash
        user.reset_token_expires_at = datetime.utcnow() + timedelta(
            minutes=RESET_TOKEN_EXPIRE_MINUTES
        )
        self.db.commit()
        self.db.refresh(user)

        return user, plain_token

    def reset_password_with_token(self, token: str, new_password: str) -> bool:
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        user = (
            self.db.query(User)
            .filter(
                User.reset_token_hash == token_hash,
                User.reset_token_expires_at > datetime.utcnow(),
            )
            .first()
        )

        if not user:
            return False

        user.hashed_password = get_password_hash(new_password)
        user.reset_token_hash = None
        user.reset_token_expires_at = None
        self.db.commit()
        return True