from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, description="User's password")


class UserRegister(BaseModel):

    email: EmailStr = Field(..., description="Student's email address")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")
    full_name: str = Field(..., min_length=2, description="Student's full name")


class Token(BaseModel):

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    must_change_password: bool = Field(default=False, description="Force password change on first login")


class ChangePassword(BaseModel):

    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=6, description="New password (min 6 chars)")


class UserResponse(BaseModel):

    id: int
    email: str
    full_name: str
    role: str
    department_id: Optional[int]
    is_active: bool
    must_change_password: bool
    phone: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[str]
    profile_picture: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)