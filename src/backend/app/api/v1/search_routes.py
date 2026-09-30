# ============================================
# CAMPUSOS - SEARCH ROUTES
# ============================================
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services.notice_service import NoticeService
from app.services.assignment_service import AssignmentService
from app.services.user_service import UserService
from app.services.department_service import DepartmentService
from app.models.user_model import User

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
async def search_all(
    q: str = Query(..., min_length=1, max_length=100),
    type: Optional[str] = Query(None),
    department_id: Optional[int] = Query(None),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Unified search across all content.
    Results filtered by user role.
    """
    results = {}

    can_search_notices = True
    can_search_assignments = True
    can_search_users = current_user.role in ["admin", "principal", "hod", "faculty"]
    can_search_departments = current_user.role in ["admin", "principal"]

    if type and type != "all":
        if type == "notices" and can_search_notices:
            results["notices"] = await search_notices(q, department_id, limit, db, current_user)
        elif type == "assignments" and can_search_assignments:
            results["assignments"] = await search_assignments(q, department_id, limit, db, current_user)
        elif type == "users" and can_search_users:
            results["users"] = await search_users(q, department_id, limit, db, current_user)
        elif type == "departments" and can_search_departments:
            results["departments"] = await search_departments(q, limit, db, current_user)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid search type: {type} or you don't have permission",
            )
    else:
        if can_search_notices:
            results["notices"] = await search_notices(q, department_id, limit, db, current_user)
        if can_search_assignments:
            results["assignments"] = await search_assignments(q, department_id, limit, db, current_user)
        if can_search_users:
            results["users"] = await search_users(q, department_id, limit, db, current_user)
        if can_search_departments:
            results["departments"] = await search_departments(q, limit, db, current_user)

    return results


# ============================================
# INTERNAL SEARCH HELPERS
# ============================================

async def search_notices(q: str, department_id: Optional[int], limit: int, db: Session, current_user: User):
    """Search notices. Services return dicts."""
    notice_service = NoticeService(db)
    notices = notice_service.search_notices(q)

    if department_id:
        notices = [n for n in notices if n.get("department_id") == department_id]

    if current_user.role == "student":
        notices = [
            n for n in notices
            if n.get("is_published") and n.get("department_id") == current_user.department_id
        ]
    elif current_user.role not in ["admin", "principal"]:
        notices = [n for n in notices if n.get("department_id") == current_user.department_id]

    notices = notices[:limit]

    return [
        {
            "id": n["id"],
            "title": n["title"],
            "content": (n["content"][:200] + "...") if n.get("content") and len(n["content"]) > 200 else n.get("content"),
            "type": "notice",
            "department_id": n.get("department_id"),
            "created_at": n.get("created_at"),
            "is_published": n.get("is_published"),
        }
        for n in notices
    ]


async def search_assignments(q: str, department_id: Optional[int], limit: int, db: Session, current_user: User):
    """Search assignments. Services return dicts."""
    assignment_service = AssignmentService(db)
    assignments = assignment_service.search_assignments(q)

    if department_id:
        assignments = [a for a in assignments if a.get("department_id") == department_id]

    if current_user.role not in ["admin", "principal"]:
        assignments = [a for a in assignments if a.get("department_id") == current_user.department_id]

    assignments = assignments[:limit]

    return [
        {
            "id": a["id"],
            "title": a["title"],
            "description": (a["description"][:200] + "...") if a.get("description") and len(a["description"]) > 200 else a.get("description"),
            "type": "assignment",
            "department_id": a.get("department_id"),
            "deadline": a.get("deadline"),
            "created_at": a.get("created_at"),
        }
        for a in assignments
    ]


async def search_users(q: str, department_id: Optional[int], limit: int, db: Session, current_user: User):
    """Search users. Services return dicts."""
    user_service = UserService(db)
    users = user_service.search_users(q)

    if department_id:
        users = [u for u in users if u.get("department_id") == department_id]

    if current_user.role == "hod":
        users = [u for u in users if u.get("department_id") == current_user.department_id]
    elif current_user.role == "faculty":
        users = [
            u for u in users
            if u.get("department_id") == current_user.department_id and u.get("role") == "student"
        ]

    users = users[:limit]

    return [
        {
            "id": u["id"],
            "full_name": u["full_name"],
            "email": u["email"],
            "role": u["role"],
            "type": "user",
            "department_id": u.get("department_id"),
        }
        for u in users
    ]


async def search_departments(q: str, limit: int, db: Session, current_user: User):
    """Search departments. Repository returns model objects."""
    department_service = DepartmentService(db)
    departments = department_service.search_departments(q)
    departments = departments[:limit]

    return [
        {
            "id": d.id,
            "name": d.name,
            "code": d.code,
            "type": "department",
            "hod_id": d.hod_id,
        }
        for d in departments
    ]