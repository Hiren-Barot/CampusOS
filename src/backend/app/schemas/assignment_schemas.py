# ============================================
# CAMPUSOS - ASSIGNMENT SCHEMAS
# ============================================
"""
Pydantic schemas for assignment management.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class AssignmentBase(BaseModel):
    """Base assignment schema."""
    title: str = Field(..., min_length=1, max_length=200, description="Assignment title")
    description: Optional[str] = Field(None, description="Assignment description")
    department_id: int = Field(..., description="Department ID")
    deadline: datetime = Field(..., description="Submission deadline")


class AssignmentCreate(AssignmentBase):
    """Assignment creation schema."""
    pass


class AssignmentUpdate(BaseModel):
    """Assignment update schema (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    deadline: Optional[datetime] = None


class AssignmentResponse(AssignmentBase):
    """Assignment response schema with author details."""
    id: int
    faculty_id: int
    faculty_name: str         
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )