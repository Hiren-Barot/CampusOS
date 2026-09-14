from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_faculty_user,
)
from app.schemas.notice_schemas import NoticeCreate, NoticeUpdate, NoticeResponse
from app.services.notice_service import NoticeService
from app.models.user_model import User

router = APIRouter(prefix="/notices", tags=["Notices"])

@router.get("/", response_model=List[NoticeResponse])
async def get_all_notices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoticeService(db)
    notices = service.get_all_notices(skip=skip, limit=limit)

    if current_user.role == "student":
        notices = [
            n for n in notices
            if n["is_published"]
            and (n["department_id"] == current_user.department_id or n["department_id"] is None)
        ]
    elif current_user.role == "faculty":
        notices = [
            n for n in notices
            if n["department_id"] in [current_user.department_id, None]
        ]
    elif current_user.role == "hod":
        notices = [
            n for n in notices
            if n["department_id"] in [current_user.department_id, None]
        ]

    if department_id:
        notices = [n for n in notices if n["department_id"] == department_id]

    return notices

@router.post("/", response_model=NoticeResponse, status_code=status.HTTP_201_CREATED)
async def create_notice(
    notice_data: NoticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    service = NoticeService(db)

    if current_user.role in ["admin", "principal"]:
        pass
    else:
        if not current_user.department_id:
            raise HTTPException(status_code=400, detail="You have no department assigned")
        notice_data.department_id = current_user.department_id

    try:
        notice = service.create_notice(notice_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return notice


@router.get("/my", response_model=List[NoticeResponse])
async def get_my_notices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoticeService(db)
    return service.get_notices_by_faculty(current_user.id)


@router.get("/published", response_model=List[NoticeResponse])
async def get_published_notices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoticeService(db)
    return service.get_published_notices()


@router.get("/search")
async def search_notices(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoticeService(db)
    notices = service.search_notices(q)

    if current_user.role == "student":
        notices = [
            n for n in notices
            if n["is_published"]
            and (n["department_id"] == current_user.department_id or n["department_id"] is None)
        ]
    elif current_user.role in ["faculty", "hod"]:
        notices = [
            n for n in notices
            if n["department_id"] in [current_user.department_id, None]
        ]

    return notices


@router.get("/department/{dept_id}", response_model=List[NoticeResponse])
async def get_notices_by_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoticeService(db)
    return service.get_notices_by_department(dept_id)


@router.get("/{notice_id}", response_model=NoticeResponse)
async def get_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoticeService(db)
    notice = service.get_notice(notice_id)

    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    if current_user.role == "student":
        if not notice["is_published"]:
            raise HTTPException(status_code=403, detail="This notice is not published")
        if notice["department_id"] not in [current_user.department_id, None]:
            raise HTTPException(status_code=403, detail="You can only view your department's notices")

    return notice


@router.put("/{notice_id}", response_model=NoticeResponse)
async def update_notice(
    notice_id: int,
    notice_data: NoticeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    service = NoticeService(db)
    notice = service.get_notice(notice_id)

    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    if not service.can_edit_notice(notice_id, current_user.id):
        raise HTTPException(status_code=403, detail="You can only edit your own notices")

    return service.update_notice(notice_id, notice_data)


@router.delete("/{notice_id}")
async def delete_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    service = NoticeService(db)
    notice = service.get_notice(notice_id)

    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    if not service.can_delete_notice(notice_id, current_user.id):
        raise HTTPException(status_code=403, detail="You can only delete your own notices")

    service.delete_notice(notice_id)
    return {"message": "Notice deleted successfully"}


@router.patch("/{notice_id}/publish")
async def publish_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    service = NoticeService(db)
    notice = service.get_notice(notice_id)

    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    if not service.can_edit_notice(notice_id, current_user.id):
        raise HTTPException(status_code=403, detail="You can only publish your own notices")

    updated = service.publish_notice(notice_id)
    return {"message": "Notice published", "notice": updated}


@router.patch("/{notice_id}/unpublish")
async def unpublish_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    service = NoticeService(db)
    notice = service.get_notice(notice_id)

    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    if not service.can_edit_notice(notice_id, current_user.id):
        raise HTTPException(status_code=403, detail="You can only unpublish your own notices")

    updated = service.unpublish_notice(notice_id)
    return {"message": "Notice unpublished", "notice": updated}