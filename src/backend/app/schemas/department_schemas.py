from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class DepartmentBase(BaseModel):


    name: str = Field(..., min_length=2, description="Department name")
    code: str = Field(..., min_length=2, max_length=10, description="Department code")
    hod_id: Optional[int] = Field(None, description="HOD user ID")


class DepartmentCreate(DepartmentBase):

    pass


class DepartmentUpdate(BaseModel):

    name: Optional[str] = Field(None, min_length=2)
    code: Optional[str] = Field(None, min_length=2, max_length=10)
    hod_id: Optional[int] = None


class DepartmentResponse(DepartmentBase):

    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )