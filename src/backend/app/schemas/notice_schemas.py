from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class NoticeBase(BaseModel):

    title: str = Field(..., min_length=1, max_length=200, description="Notice title")
    content: str = Field(..., min_length=1, description="Notice content")
    department_id: int = Field(..., description="Department ID")
    is_published: bool = Field(default=True, description="Publish status")


class NoticeCreate(NoticeBase):

    pass


class NoticeUpdate(BaseModel):

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    is_published: Optional[bool] = None


class NoticeResponse(NoticeBase):

    id: int
    faculty_id: int
    faculty_name: Optional[str] = None         
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )