from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

from app.schemas.profile_schemas import ProfileCreate, ProfileUpdate, ProfileResponse


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2)
    role: str = Field(default="student")
    department_id: Optional[int] = None


class UserCreate(UserBase):
    profile: Optional[ProfileCreate] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None
    profile: Optional[ProfileUpdate] = None


class UserResponse(UserBase):
    id: int
    department_name: Optional[str] = None
    is_active: bool
    must_change_password: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    temp_password: Optional[str] = None
    profile: Optional[ProfileResponse] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)