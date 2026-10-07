from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.query_schemas import QueryCreate, QueryReply, QueryResponse
from app.services.query_service import QueryService
from app.models.user_model import User

router = APIRouter(prefix="/queries", tags=["Queries"])


@router.post("/", response_model=QueryResponse, status_code=status.HTTP_201_CREATED)
async def create_query(
    data: QueryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can create queries")

    service = QueryService(db)
    try:
        return service.create_query(data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[QueryResponse])
async def get_queries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = QueryService(db)
    return service.get_queries_for_user(current_user)


@router.get("/{query_id}", response_model=QueryResponse)
async def get_query(
    query_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = QueryService(db)
    query = service.get_query(query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    if not service.can_view_query(query, current_user):
        raise HTTPException(status_code=403, detail="Access denied")
    return query


@router.post("/{query_id}/reply", response_model=QueryResponse)
async def reply_to_query(
    query_id: int,
    data: QueryReply,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["faculty", "hod"]:
        raise HTTPException(status_code=403, detail="Only faculty or HOD can reply")

    service = QueryService(db)
    try:
        result = service.reply_to_query(query_id, data, current_user.id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail="Query not found")
    return result


@router.delete("/{query_id}")
async def delete_query(
    query_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = QueryService(db)
    try:
        ok = service.delete_query(query_id, current_user.id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not ok:
        raise HTTPException(status_code=404, detail="Query not found")
    return {"message": "Query deleted successfully"}