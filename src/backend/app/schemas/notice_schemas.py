# ============================================
# CAMPUSOS - NOTICE SCHEMAS
# ============================================
"""
Pydantic schemas for notice management.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class NoticeBase(BaseModel):
    """Base notice schema."""
    title: str = Field(..., min_length=1, max_length=200, description="Notice title")
    content: str = Field(..., min_length=1, description="Notice content")
    department_id: int = Field(..., description="Department ID")
    is_published: bool = Field(default=True, description="Publish status")


class NoticeCreate(NoticeBase):
    """Notice creation schema."""
    pass


class NoticeUpdate(BaseModel):
    """Notice update schema (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    is_published: Optional[bool] = None


class NoticeResponse(NoticeBase):
    """Notice response schema with author details."""
    id: int
    faculty_id: int
    faculty_name: str         
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )