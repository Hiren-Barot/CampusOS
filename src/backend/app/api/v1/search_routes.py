from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

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
    q: str = Query(..., min_length=1, max_length=100, description="Search query"),
    type: Optional[str] = Query(
        None,
        description="Filter by type: notices, assignments, users, departments, all"
    ),
    department_id: Optional[int] = Query(
        None,
        description="Filter by department ID"
    ),
    limit: int = Query(20, ge=1, le=50, description="Results per category"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    results = {}
    
    can_search_notices = True
    can_search_assignments = True
    can_search_users = False
    can_search_departments = False
    
    if current_user.role == "admin":
        can_search_users = True
        can_search_departments = True
    elif current_user.role == "principal":
        can_search_users = True
        can_search_departments = True
    elif current_user.role == "hod":
        can_search_users = True
    elif current_user.role == "faculty":
        can_search_users = True

    if type and type != "all":
        if type == "notices" and can_search_notices:
            results["notices"] = await search_notices(
                q=q,
                department_id=department_id,
                limit=limit,
                db=db,
                current_user=current_user,
            )
        elif type == "assignments" and can_search_assignments:
            results["assignments"] = await search_assignments(
                q=q,
                department_id=department_id,
                limit=limit,
                db=db,
                current_user=current_user,
            )
        elif type == "users" and can_search_users:
            results["users"] = await search_users(
                q=q,
                department_id=department_id,
                limit=limit,
                db=db,
                current_user=current_user,
            )
        elif type == "departments" and can_search_departments:
            results["departments"] = await search_departments(
                q=q,
                limit=limit,
                db=db,
                current_user=current_user,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid search type: {type} or you don't have permission",
            )
    else:
        if can_search_notices:
            results["notices"] = await search_notices(
                q=q,
                department_id=department_id,
                limit=limit,
                db=db,
                current_user=current_user,
            )
        
        if can_search_assignments:
            results["assignments"] = await search_assignments(
                q=q,
                department_id=department_id,
                limit=limit,
                db=db,
                current_user=current_user,
            )
        
        if can_search_users:
            results["users"] = await search_users(
                q=q,
                department_id=department_id,
                limit=limit,
                db=db,
                current_user=current_user,
            )
        
        if can_search_departments:
            results["departments"] = await search_departments(
                q=q,
                limit=limit,
                db=db,
                current_user=current_user,
            )
    
    return results


async def search_notices(q: str, department_id: Optional[int], limit: int, db: Session, current_user: User):
    notice_service = NoticeService(db)
    notices = notice_service.search_notices(q)
    
    if department_id:
        notices = [n for n in notices if n.department_id == department_id]
    
    if current_user.role == "student":
        notices = [n for n in notices if n.is_published and n.department_id == current_user.department_id]
    elif current_user.role not in ["admin", "principal"]:
        notices = [n for n in notices if n.department_id == current_user.department_id]
    
    notices = notices[:limit]
    
    return [
        {
            "id": n.id,
            "title": n.title,
            "content": n.content[:200] + "..." if len(n.content) > 200 else n.content,
            "type": "notice",
            "department_id": n.department_id,
            "created_at": n.created_at,
            "is_published": n.is_published,
        }
        for n in notices
    ]


async def search_assignments(
        q: str,
        department_id: Optional[int],
        limit: int,
        db: Session,
      current_user: User
    ):
    assignment_service = AssignmentService(db)
    assignments = assignment_service.search_assignments(q)
    
    if department_id:
        assignments = [a for a in assignments if a.department_id == department_id]
    
    if current_user.role not in ["admin", "principal"]:
        assignments = [a for a in assignments if a.department_id == current_user.department_id]
    
    assignments = assignments[:limit]
    
    return [
        {
            "id": a.id,
            "title": a.title,
            "description": a.description[:200] + "..." if a.description and len(a.description) > 200 else a.description,
            "type": "assignment",
            "department_id": a.department_id,
            "deadline": a.deadline,
            "created_at": a.created_at,
        }
        for a in assignments
    ]


async def search_users(
        q: str, 
        department_id: Optional[int], 
        limit: int, 
        db: Session, current_user: User
    ):
    user_service = UserService(db)
    users = user_service.search_users(q)
    
    if department_id:
        users = [u for u in users if u.department_id == department_id]
    
    if current_user.role == "hod":
        users = [u for u in users if u.department_id == current_user.department_id]
    elif current_user.role == "faculty":
        users = [u for u in users if u.department_id == current_user.department_id and u.role == "student"]
    
    users = users[:limit]
    
    return [
        {
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "role": u.role,
            "type": "user",
            "department_id": u.department_id,
        }
        for u in users
    ]


async def search_departments(q: str, limit: int, db: Session, current_user: User):
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