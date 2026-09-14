from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_faculty_user,
)
from app.schemas.assignment_schemas import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
)
from app.services.assignment_service import AssignmentService
from app.models.user_model import User

router = APIRouter(prefix="/assignments", tags=["Assignments"])


def _require_faculty_only(current_user: User):
    if current_user.role != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only faculty can manage assignments",
        )


@router.get("/", response_model=List[AssignmentResponse])
async def get_all_assignments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AssignmentService(db)
    assignments = service.get_all_assignments(skip=skip, limit=limit)

    if current_user.role == "student":
        assignments = [
            a for a in assignments
            if a["department_id"] == current_user.department_id
            or a["department_id"] is None
        ]
    elif current_user.role == "faculty":
        assignments = [
            a for a in assignments
            if a["faculty_id"] == current_user.id
            or a["department_id"] == current_user.department_id
        ]
    elif current_user.role == "hod":
        assignments = [
            a for a in assignments
            if a["department_id"] == current_user.department_id
        ]

    if department_id:
        assignments = [a for a in assignments if a["department_id"] == department_id]

    return assignments


@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    _require_faculty_only(current_user)

    if not assignment_data.department_id:
        assignment_data.department_id = current_user.department_id

    if not assignment_data.department_id:
        raise HTTPException(status_code=400, detail="Department is required")

    if assignment_data.department_id != current_user.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create assignments in your own department",
        )

    service = AssignmentService(db)
    return service.create_assignment(assignment_data, current_user.id)


@router.get("/my", response_model=List[AssignmentResponse])
async def get_my_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AssignmentService(db)
    return service.get_assignments_by_faculty(current_user.id)


@router.get("/upcoming", response_model=List[AssignmentResponse])
async def get_upcoming_assignments(
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AssignmentService(db)

    if not department_id and current_user.role not in ["admin", "principal"]:
        department_id = current_user.department_id

    assignments = service.get_upcoming_assignments(department_id)

    if current_user.role == "student":
        assignments = [
            a for a in assignments
            if a["department_id"] == current_user.department_id or a["department_id"] is None
        ]

    return assignments


@router.get("/search")
async def search_assignments(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AssignmentService(db)
    assignments = service.search_assignments(q)

    if current_user.role == "student":
        assignments = [
            a for a in assignments
            if a["department_id"] == current_user.department_id or a["department_id"] is None
        ]
    elif current_user.role in ["faculty", "hod"]:
        assignments = [
            a for a in assignments
            if a["department_id"] == current_user.department_id
        ]

    return assignments


@router.get("/department/{dept_id}", response_model=List[AssignmentResponse])
async def get_assignments_by_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AssignmentService(db)
    return service.get_assignments_by_department(dept_id)


@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AssignmentService(db)
    assignment = service.get_assignment(assignment_id)

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if current_user.role == "student":
        if assignment["department_id"] not in [current_user.department_id, None]:
            raise HTTPException(status_code=403, detail="Access denied")

    return assignment


@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: int,
    assignment_data: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    _require_faculty_only(current_user)

    service = AssignmentService(db)
    assignment = service.get_assignment(assignment_id)

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if assignment["faculty_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own assignments")

    return service.update_assignment(assignment_id, assignment_data)


@router.delete("/{assignment_id}")
async def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    _require_faculty_only(current_user)

    service = AssignmentService(db)
    assignment = service.get_assignment(assignment_id)

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if assignment["faculty_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own assignments")

    service.delete_assignment(assignment_id)
    return {"message": "Assignment deleted successfully"}