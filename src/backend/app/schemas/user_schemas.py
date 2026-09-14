from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(..., min_length=2, description="User's full name")
    role: str = Field(default="student", description="User role")
    department_id: Optional[int] = Field(None, description="Department ID")


class UserCreate(BaseModel):
    """Admin creates user schema."""
    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(..., min_length=2, description="User's full name")
    role: str = Field(default="student", description="User role")
    department_id: Optional[int] = Field(None, description="Department ID")


class UserUpdate(BaseModel):
    """User update schema."""
    full_name: Optional[str] = Field(None, min_length=2)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    profile_picture: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    is_active: bool
    must_change_password: bool
    phone: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime
    temp_password: Optional[str] = None 

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)