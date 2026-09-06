from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_faculty_user,
    get_hod_user,
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
    notice_service = NoticeService(db)
    
    if current_user.role == "student":
        if department_id:
            if current_user.department_id != department_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view notices from your own department",
                )
            notices = notice_service.get_notices_by_department(department_id)
        else:
            notices = notice_service.get_published_notices()

            notices = [n for n in notices if n.department_id == current_user.department_id]
    else:

        if department_id:
            if current_user.role not in ["admin", "principal"]:
                if current_user.department_id != department_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You can only view notices from your own department",
                    )
            notices = notice_service.get_all_notices(skip=skip, limit=limit)

            notices = [n for n in notices if n.department_id == department_id]
        else:
            notices = notice_service.get_all_notices(skip=skip, limit=limit)
            
            if current_user.role not in ["admin", "principal"]:
                notices = [n for n in notices if n.department_id == current_user.department_id]
    
    return notices


@router.post("/", response_model=NoticeResponse, status_code=status.HTTP_201_CREATED)
async def create_notice(
    notice_data: NoticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    notice_service = NoticeService(db)
    
    if current_user.role not in ["admin", "principal"]:
        if current_user.department_id != notice_data.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only post notices in your own department",
            )
    
    notice = notice_service.create_notice(notice_data, current_user.id)
    return notice


@router.get("/search")
async def search_notices(
    q: str = Query(..., min_length=1),
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notice_service = NoticeService(db)
    
    if current_user.role == "student":
        notices = notice_service.search_notices(q)
        notices = [n for n in notices if n.is_published and n.department_id == current_user.department_id]
    else:
        notices = notice_service.search_notices(q)
        if current_user.role not in ["admin", "principal"]:
            notices = [n for n in notices if n.department_id == current_user.department_id]
        
        if department_id:
            notices = [n for n in notices if n.department_id == department_id]
    
    return notices

@router.get("/{notice_id}", response_model=NoticeResponse)
async def get_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notice_service = NoticeService(db)
    notice = notice_service.get_notice(notice_id)
    
    if not notice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
        )
    
    if current_user.role == "student":
        if not notice.is_published:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This notice is not published",
            )
        if current_user.department_id != notice.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view notices from your own department",
            )
    else:
        if current_user.role not in ["admin", "principal"]:
            if current_user.department_id != notice.department_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view notices from your own department",
                )
    
    return notice


@router.put("/{notice_id}", response_model=NoticeResponse)
async def update_notice(
    notice_id: int,
    notice_data: NoticeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    notice_service = NoticeService(db)
    notice = notice_service.get_notice(notice_id)
    
    if not notice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
        )
    
    if not notice_service.can_edit_notice(notice_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this notice",
        )
    
    updated_notice = notice_service.update_notice(notice_id, notice_data)
    return updated_notice


@router.delete("/{notice_id}")
async def delete_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    notice_service = NoticeService(db)
    notice = notice_service.get_notice(notice_id)
    
    if not notice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
        )
    
    if not notice_service.can_delete_notice(notice_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this notice",
        )
    
    notice_service.delete_notice(notice_id)
    return {"message": "Notice deleted successfully"}


@router.patch("/{notice_id}/publish")
async def publish_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    notice_service = NoticeService(db)
    notice = notice_service.get_notice(notice_id)
    
    if not notice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
        )
    
    if not notice_service.can_edit_notice(notice_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to publish this notice",
        )
    
    updated_notice = notice_service.publish_notice(notice_id)
    return {
        "message": "Notice published successfully",
        "notice": updated_notice
    }


@router.patch("/{notice_id}/unpublish")
async def unpublish_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_faculty_user),
):
    notice_service = NoticeService(db)
    notice = notice_service.get_notice(notice_id)
    
    if not notice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
        )
    
    if not notice_service.can_edit_notice(notice_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to unpublish this notice",
        )
    
    updated_notice = notice_service.unpublish_notice(notice_id)
    return {
        "message": "Notice unpublished successfully",
        "notice": updated_notice
    }
