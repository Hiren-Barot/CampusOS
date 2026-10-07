import os
import uuid
from pathlib import Path
from datetime import datetime as _dt

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query,
    File,
    UploadFile,
    Form,
)
from fastapi.responses import FileResponse
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
from app.models.assignment_model import Assignment

router = APIRouter(prefix="/assignments", tags=["Assignments"])

UPLOAD_DIR = Path("uploads/assignments")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024 
ALLOWED_EXTENSIONS = {".pdf", ".ppt", ".pptx", ".doc", ".docx", ".jpg", ".jpeg", ".png"}

def _require_faculty_only(current_user: User):
    if current_user.role != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only faculty can manage assignments",
        )

def _validate_upload(file: UploadFile) -> str:
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )
    return ext


async def _save_upload(file: UploadFile):
    ext = _validate_upload(file)
    contents = await file.read()
    size = len(contents)
    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size / 1024 / 1024:.1f} MB). Max 10 MB.",
        )
    safe_name = f"{uuid.uuid4().hex}{ext}"
    disk_path = UPLOAD_DIR / safe_name
    with open(disk_path, "wb") as f:
        f.write(contents)
    return str(disk_path), file.filename, size

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

@router.get("/{assignment_id}/download")
async def download_assignment_file(
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

    model = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not model or not model.file_path:
        raise HTTPException(status_code=404, detail="No file attached to this assignment")

    disk_path = Path(model.file_path)
    if not disk_path.exists():
        raise HTTPException(status_code=404, detail="File missing on server")

    return FileResponse(
        path=disk_path,
        filename=model.file_name or disk_path.name,
        media_type=model.file_type or "application/octet-stream",
    )


# ============================================================
#  GET SINGLE
# ============================================================

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

@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    deadline: str = Form(...),
    department_id: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    _require_faculty_only(current_user)

    try:
        deadline_dt = _dt.fromisoformat(deadline.replace("Z", "+00:00"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid deadline format")

    dept = department_id or current_user.department_id
    if not dept:
        raise HTTPException(status_code=400, detail="Department is required")
    if dept != current_user.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create assignments in your own department",
        )

    file_path = file_name = file_type = None
    file_size = None

    if file and file.filename:
        file_path, file_name, file_size = await _save_upload(file)
        file_type = file.content_type

    assignment_data = AssignmentCreate(
        title=title,
        description=description,
        department_id=dept,
        deadline=deadline_dt,
    )

    service = AssignmentService(db)
    return service.create_assignment(
        assignment_data,
        current_user.id,
        file_path=file_path,
        file_name=file_name,
        file_size=file_size,
        file_type=file_type,
    )

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