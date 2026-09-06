from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_faculty_user,
    get_hod_user,
)
from app.schemas.assignment_schemas import AssignmentCreate, AssignmentUpdate, AssignmentResponse
from app.services.assignment_service import AssignmentService
from app.models.user_model import User

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.get("/", response_model=List[AssignmentResponse])
async def get_all_assignments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment_service = AssignmentService(db)
    
    if department_id:
        if current_user.role not in ["admin", "principal"]:
            if current_user.department_id != department_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view assignments from your own department",
                )
        assignments = assignment_service.get_assignments_by_department(department_id)
    else:
        assignments = assignment_service.get_all_assignments(skip=skip, limit=limit)
        
        if current_user.role not in ["admin", "principal"]:
            assignments = [a for a in assignments if a.department_id == current_user.department_id]
    
    return assignments


@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    assignment_service = AssignmentService(db)
    
    if current_user.role not in ["admin", "principal"]:
        if current_user.department_id != assignment_data.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only post assignments in your own department",
            )
    
    assignment = assignment_service.create_assignment(assignment_data, current_user.id)
    return assignment


@router.get("/search")
async def search_assignments(
    q: str = Query(..., min_length=1),
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment_service = AssignmentService(db)
    
    assignments = assignment_service.search_assignments(q)
    
    if current_user.role not in ["admin", "principal"]:
        assignments = [a for a in assignments if a.department_id == current_user.department_id]
    
    if department_id:
        if current_user.role not in ["admin", "principal"]:
            if current_user.department_id != department_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only search assignments from your own department",
                )
        assignments = [a for a in assignments if a.department_id == department_id]
    
    return assignments

@router.get("/upcoming", response_model=List[AssignmentResponse])
async def get_upcoming_assignments(
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment_service = AssignmentService(db)
    
    if department_id:
        if current_user.role not in ["admin", "principal"]:
            if current_user.department_id != department_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view assignments from your own department",
                )
    else:
        department_id = current_user.department_id if current_user.role not in ["admin", "principal"] else None
    
    assignments = assignment_service.get_upcoming_assignments(department_id)
    return assignments


@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment_service = AssignmentService(db)
    assignment = assignment_service.get_assignment(assignment_id)
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found",
        )
    
    if current_user.role not in ["admin", "principal"]:
        if current_user.department_id != assignment.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view assignments from your own department",
            )
    
    return assignment


@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: int,
    assignment_data: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    assignment_service = AssignmentService(db)
    assignment = assignment_service.get_assignment(assignment_id)
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found",
        )
    
    if not assignment_service.can_edit_assignment(assignment_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this assignment",
        )
    
    updated_assignment = assignment_service.update_assignment(assignment_id, assignment_data)
    return updated_assignment


@router.delete("/{assignment_id}")
async def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    assignment_service = AssignmentService(db)
    assignment = assignment_service.get_assignment(assignment_id)
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found",
        )
    
    if not assignment_service.can_delete_assignment(assignment_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this assignment",
        )
    
    assignment_service.delete_assignment(assignment_id)
    return {"message": "Assignment deleted successfully"}
