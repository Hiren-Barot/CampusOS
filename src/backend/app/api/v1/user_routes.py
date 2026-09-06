from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_admin_user,
    get_principal_user,
    get_hod_user,
    get_faculty_user,
    check_user_can_manage_user,
    check_user_can_view_user,
)
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.models.user_model import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    role: Optional[str] = None,
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_principal_user), 
):
    user_service = UserService(db)
    
    filters = {}
    if role:
        filters["role"] = role
    if department_id:
        filters["department_id"] = department_id
    
    users = user_service.get_all_users(skip=skip, limit=limit, **filters)
    
    if current_user.role == "hod":
        users = [u for u in users if u.department_id == current_user.department_id]
    
    return users


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_principal_user),
):
    if user_data.role not in ["admin", "principal"] and not user_data.department_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department ID is required for role: {user_data.role}",
        )
    
    user_service = UserService(db)
    user, temp_password = user_service.create_user(user_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    
    response = UserResponse.model_validate(user)
    response.temp_password = temp_password
    return response


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user



@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_principal_user),
):
    user_service = UserService(db)
    target_user = user_service.get_user(user_id)
    
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not check_user_can_manage_user(target_user, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this user",
        )
    
    updated_user = user_service.update_user(user_id, user_data)
    return updated_user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    user_service = UserService(db)
    target_user = user_service.get_user(user_id)
    
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if target_user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete yourself",
        )
    
    if target_user.role == "admin":
        admins = user_service.get_users_by_role("admin")
        if len(admins) <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete the only admin user",
            )
    
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return {"message": "User deactivated successfully"}


@router.delete("/{user_id}/permanent")
async def hard_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    user_service = UserService(db)
    target_user = user_service.get_user(user_id)
    
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if target_user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete yourself",
        )
    
    if target_user.role == "admin":
        admins = user_service.get_users_by_role("admin")
        if len(admins) <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete the only admin user",
            )
    
    success = user_service.hard_delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return {"message": "User permanently deleted"}


@router.get("/search")
async def search_users(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_principal_user),
):
    user_service = UserService(db)
    users = user_service.search_users(q)
    
    if current_user.role == "hod":
        users = [u for u in users if u.department_id == current_user.department_id]
    
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    target_user = user_service.get_user(user_id)
    
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not check_user_can_view_user(target_user, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this user",
        )
    
    return target_user

@router.get("/department/{department_id}", response_model=List[UserResponse])
async def get_users_by_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_hod_user),
):
    user_service = UserService(db)
    
    if current_user.role == "hod" and current_user.department_id != department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own department",
        )
    
    if current_user.role == "faculty" and current_user.department_id != department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own department",
        )
    
    if current_user.role == "faculty":
        users = user_service.get_students_by_department(department_id)
    else:
        users = user_service.get_users_by_department(department_id)
    
    return users


@router.get("/department/{department_id}/faculty", response_model=List[UserResponse])
async def get_faculty_by_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_hod_user),
):
    user_service = UserService(db)
    
    if current_user.role == "hod" and current_user.department_id != department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own department",
        )
    
    users = user_service.get_faculty_by_department(department_id)
    return users


@router.get("/department/{department_id}/students", response_model=List[UserResponse])
async def get_students_by_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    user_service = UserService(db)
    
    if current_user.role not in ["admin", "principal"]:
        if current_user.department_id != department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own department",
            )
    
    users = user_service.get_students_by_department(department_id)
    return users