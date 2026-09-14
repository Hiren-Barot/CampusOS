from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class NoticeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    department_id: Optional[int] = Field(None, description="None = all departments")
    is_published: bool = Field(default=True)


class NoticeCreate(NoticeBase):
    pass


class NoticeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    department_id: Optional[int] = None
    is_published: Optional[bool] = None


class NoticeResponse(NoticeBase):
    id: int
    faculty_id: int
    faculty_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)