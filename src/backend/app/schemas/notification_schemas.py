from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class NotificationBase(BaseModel):

    title: str = Field(..., min_length=1, max_length=200, description="Notification title")
    message: str = Field(..., min_length=1, description="Notification message")
    type: str = Field(..., description="Notification type: notice, assignment, deadline, system")
    related_id: Optional[int] = Field(None, description="ID of related entity (notice_id or assignment_id)")


class NotificationCreate(BaseModel):

    user_id: int = Field(..., description="User ID receiving notification")
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1)
    type: str = Field(...)
    related_id: Optional[int] = None


class NotificationUpdate(BaseModel):

    is_read: Optional[bool] = None


class NotificationResponse(NotificationBase):

    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class NotificationCount(BaseModel):

    count: int = Field(..., description="Number of unread notifications")