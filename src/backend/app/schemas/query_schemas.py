from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class QueryBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)


class QueryCreate(QueryBase):
    pass


class QueryReply(BaseModel):
    reply: str = Field(..., min_length=1)


class QueryResponse(QueryBase):
    id: int
    student_id: int
    student_name: Optional[str] = None
    department_id: int
    department_name: Optional[str] = None
    reply: Optional[str] = None
    replied_by_id: Optional[int] = None
    replied_by_name: Optional[str] = None
    replied_at: Optional[datetime] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )