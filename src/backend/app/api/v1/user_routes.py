from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    check_user_can_manage_user,
    check_user_can_view_user,
)
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.models.user_model import User

router = APIRouter(prefix="/users", tags=["Users"])

def _check_create_permission(current_user: User, target_role: str, target_dept_id):
    ROLE_RANK = {"student": 1, "faculty": 2, "hod": 3, "principal": 4, "admin": 5}
    my_rank = ROLE_RANK.get(current_user.role, 0)
    target_rank = ROLE_RANK.get(target_role, 0)

    if current_user.role == "admin":
        return True

    if current_user.role == "principal":
        return target_role != "admin"

    if current_user.role == "hod":
        if target_role not in ["faculty", "student"]:
            return False
        if target_dept_id != current_user.department_id:
            return False
        return True

    if current_user.role == "faculty":
        if target_role != "student":
            return False
        if target_dept_id != current_user.department_id:
            return False
        return True

    return False

@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    role: Optional[str] = None,
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)

    filters = {}
    if role:
        filters["role"] = role
    if department_id:
        filters["department_id"] = department_id

    users = service.get_all_users(skip=skip, limit=limit, **filters)

    if current_user.role in ["admin", "principal"]:
        pass
    elif current_user.role == "hod":
        users = [u for u in users if u.get("department_id") == current_user.department_id]
    elif current_user.role == "faculty":
        users = [
            u for u in users
            if u.get("department_id") == current_user.department_id
            and u.get("role") == "student"
        ]
    else:
        users = []

    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_data.email = user_data.email.strip().lower()
    user_data.full_name = user_data.full_name.strip()

    if current_user.role in ["hod", "faculty"]:
        if not current_user.department_id:
            raise HTTPException(status_code=400, detail="You have no department assigned")
        user_data.department_id = current_user.department_id

    if not _check_create_permission(current_user, user_data.role, user_data.department_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role '{current_user.role}' cannot create role '{user_data.role}'",
        )

    if user_data.role not in ["admin", "principal"] and not user_data.department_id:
        raise HTTPException(status_code=400, detail="Department is required")

    service = UserService(db)
    user, temp_password = service.create_user(user_data)

    if not user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    response_data = service._enrich_user(user)
    response_data["temp_password"] = temp_password
    return response_data


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return service._enrich_user(current_user)


@router.get("/search")
async def search_users(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    users = service.search_users(q)

    if current_user.role == "hod":
        users = [u for u in users if u.get("department_id") == current_user.department_id]
    elif current_user.role == "faculty":
        users = [
            u for u in users
            if u.get("department_id") == current_user.department_id
            and u.get("role") == "student"
        ]
    elif current_user.role == "student":
        users = []

    return users


@router.get("/department/{department_id}", response_model=List[UserResponse])
async def get_users_by_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["admin", "principal"]:
        if current_user.department_id != department_id:
            raise HTTPException(status_code=403, detail="Access denied")

    service = UserService(db)
    users = service.get_users_by_department(department_id)

    if current_user.role == "faculty":
        users = [u for u in users if u.get("role") == "student"]

    return users


@router.get("/department/{department_id}/faculty", response_model=List[UserResponse])
async def get_faculty_by_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["admin", "principal"]:
        if current_user.department_id != department_id:
            raise HTTPException(status_code=403, detail="Access denied")

    service = UserService(db)
    return service.get_faculty_by_department(department_id)


@router.get("/department/{department_id}/students", response_model=List[UserResponse])
async def get_students_by_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["admin", "principal"]:
        if current_user.department_id != department_id:
            raise HTTPException(status_code=403, detail="Access denied")

    service = UserService(db)
    return service.get_students_by_department(department_id)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    target_user = service.get_user(user_id)

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not check_user_can_view_user(target_user, current_user):
        raise HTTPException(status_code=403, detail="Access denied")

    return service._enrich_user(target_user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    target_user = service.get_user(user_id)

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    is_self = target_user.id == current_user.id
    if not is_self and not check_user_can_manage_user(target_user, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to update this user")

    updated = service.update_user(user_id, user_data)
    return service._enrich_user(updated)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    target_user = service.get_user(user_id)

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if target_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot delete yourself")

    if not check_user_can_manage_user(target_user, current_user):
        raise HTTPException(
            status_code=403,
            detail=f"Role '{current_user.role}' cannot delete role '{target_user.role}'",
        )

    if target_user.role == "admin":
        admins = service.get_users_by_role("admin")
        if len(admins) <= 1:
            raise HTTPException(status_code=400, detail="Cannot delete the only admin")

    success = service.hard_delete_user(user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete user")

    return {"message": "User deleted successfully"}