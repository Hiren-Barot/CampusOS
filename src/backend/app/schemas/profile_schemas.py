from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, date


class ProfileBase(BaseModel):
    phone: Optional[str] = Field(None, max_length=20)
    gender: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[date] = None
    address: Optional[str] = Field(None, max_length=500)

    enrollment_no: Optional[str] = Field(None, max_length=50)
    course: Optional[str] = Field(None, max_length=100)
    semester: Optional[int] = Field(None, ge=1, le=12)
    admission_year: Optional[int] = Field(None, ge=2000, le=2100)
    parent_name: Optional[str] = Field(None, max_length=100)
    parent_phone: Optional[str] = Field(None, max_length=20)

    qualification: Optional[str] = Field(None, max_length=100)
    specialization: Optional[str] = Field(None, max_length=150)
    experience_years: Optional[int] = Field(None, ge=0, le=60)
    joining_date: Optional[date] = None
    designation: Optional[str] = Field(None, max_length=100)


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)