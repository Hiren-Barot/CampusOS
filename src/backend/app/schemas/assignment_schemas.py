from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class AssignmentBase(BaseModel):

    title: str = Field(..., min_length=1, max_length=200, description="Assignment title")
    description: Optional[str] = Field(None, description="Assignment description")
    department_id: int = Field(..., description="Department ID")
    deadline: datetime = Field(..., description="Submission deadline")


class AssignmentCreate(AssignmentBase):

    pass


class AssignmentUpdate(BaseModel):

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    deadline: Optional[datetime] = None


class AssignmentResponse(AssignmentBase):

    id: int
    faculty_id: int
    faculty_name: Optional[str] = None         
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )