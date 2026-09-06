from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.core.security.jwt import decode_token
from app.models.user_model import User
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)

security = HTTPBearer(
    scheme_name="Bearer",
    description="Enter your JWT token: Bearer <token>",
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    
    token = credentials.credentials
    
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_repo = UserRepository(db)
    user = user_repo.get(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )
    
    return user


def require_role(allowed_roles: List[str]):
   
    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' not allowed. "
                       f"Required: {', '.join(allowed_roles)}",
            )
        return current_user
    
    return role_checker


async def get_admin_user(
    current_user: User = Depends(require_role(["admin"])),
) -> User:
    return current_user


async def get_principal_user(
    current_user: User = Depends(require_role(["admin", "principal"])),
) -> User:
    return current_user


async def get_hod_user(
    current_user: User = Depends(require_role(["admin", "principal", "hod"])),
) -> User:
    return current_user


async def get_faculty_user(
    current_user: User = Depends(require_role(["admin", "principal", "hod", "faculty"])),
) -> User:
    return current_user


async def get_student_user(
    current_user: User = Depends(require_role(["admin", "principal", "hod", "faculty", "student"])),
) -> User:
    return current_user


def check_user_in_department(user: User, department_id: int) -> bool:
    if user.role in ["admin", "principal"]:
        return True
    return user.department_id == department_id


def check_user_can_manage_user(target_user: User, current_user: User) -> bool:
    if current_user.role == "admin":
        return True
    
    if current_user.role == "principal":
        return target_user.role != "admin"
    
    if current_user.role == "hod":
        if target_user.role in ["admin", "principal", "hod"]:
            return False
        return target_user.department_id == current_user.department_id
    
    if current_user.role == "faculty":
        if target_user.role != "student":
            return False
        return target_user.department_id == current_user.department_id
    
    return False


def check_user_can_view_user(target_user: User, current_user: User) -> bool:

    if current_user.role in ["admin", "principal"]:
        return True
    
    if current_user.role == "hod":
        return target_user.department_id == current_user.department_id
    
    if current_user.role == "faculty":
        if target_user.role not in ["faculty", "student"]:
            return False
        return target_user.department_id == current_user.department_id
    
    if current_user.role == "student":
        return target_user.id == current_user.id
    
    return False