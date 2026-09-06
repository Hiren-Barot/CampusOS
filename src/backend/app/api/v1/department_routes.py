from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_admin_user,
    get_principal_user,
    get_hod_user,
    check_user_in_department,
)
from app.schemas.department_schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.services.department_service import DepartmentService
from app.models.user_model import User

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/", response_model=List[DepartmentResponse])
async def get_all_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dept_service = DepartmentService(db)
    departments = dept_service.get_all_departments(skip=skip, limit=limit)
    return departments


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    dept_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_principal_user),
):
    dept_service = DepartmentService(db)
    department = dept_service.create_department(dept_data)
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department with this code already exists",
        )
    
    return department


@router.get("/search")
async def search_departments(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dept_service = DepartmentService(db)
    departments = dept_service.search_departments(q)
    return departments

@router.get("/{dept_id}", response_model=DepartmentResponse)
async def get_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dept_service = DepartmentService(db)
    department = dept_service.get_department(dept_id)
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    return department


@router.put("/{dept_id}", response_model=DepartmentResponse)
async def update_department(
    dept_id: int,
    dept_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_principal_user), 
):
    dept_service = DepartmentService(db)
    department = dept_service.get_department(dept_id)
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    updated_dept = dept_service.update_department(dept_id, dept_data)
    return updated_dept


@router.delete("/{dept_id}")
async def delete_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_principal_user),
):
    dept_service = DepartmentService(db)
    department = dept_service.get_department(dept_id)
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    from app.repositories.user_repository import UserRepository
    user_repo = UserRepository(db)
    users = user_repo.get_by_department(dept_id)
    
    if users:
        for user in users:
            user_repo.update(user.id, department_id=None)
    
    success = dept_service.delete_department(dept_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete department",
        )
    
    return {"message": "Department deleted successfully"}


@router.get("/{dept_id}/stats")
async def get_department_stats(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_hod_user),
):
    dept_service = DepartmentService(db)
    department = dept_service.get_department(dept_id)
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    if current_user.role not in ["admin", "principal"]:
        if current_user.department_id != dept_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own department",
            )
    
    stats = dept_service.get_department_stats(dept_id)
    return stats


@router.post("/{dept_id}/hod/{hod_id}")
async def assign_hod(
    dept_id: int,
    hod_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_principal_user),  
):
    dept_service = DepartmentService(db)
    department = dept_service.get_department(dept_id)
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    from app.repositories.user_repository import UserRepository
    user_repo = UserRepository(db)
    user = user_repo.get(hod_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if user.role not in ["admin", "principal", "hod", "faculty"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be faculty or above to be HOD",
        )
    
    updated_dept = dept_service.assign_hod(dept_id, hod_id)
    
    if not updated_dept:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign HOD",
        )
    
    if user.role != "hod":
        user_repo.update(hod_id, role="hod")
    
    return {
        "message": f"HOD assigned successfully",
        "department": updated_dept.name,
        "hod_name": user.full_name
    }


@router.delete("/{dept_id}/hod")
async def remove_hod(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_principal_user),
):
    dept_service = DepartmentService(db)
    department = dept_service.get_department(dept_id)
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    if not department.hod_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This department doesn't have a HOD assigned",
        )
    
    from app.repositories.user_repository import UserRepository
    user_repo = UserRepository(db)
    hod_user = user_repo.get(department.hod_id)
    
    from app.schemas.department_schemas import DepartmentUpdate

    updated_dept = dept_service.update_department(
        dept_id, 
        DepartmentUpdate(hod_id=None)
    )
    
    if hod_user and hod_user.role == "hod":
        user_repo.update(hod_user.id, role="faculty")
    
    return {
        "message": "HOD removed successfully",
        "department": updated_dept.name
    }
