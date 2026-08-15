# ============================================
# CAMPUSOS - SCHEMAS
# ============================================
"""
Pydantic schemas for request/response validation.
Export all schemas for clean imports.
"""

# Auth
from .auth import (
    UserLogin,
    UserRegister,
    Token,
    ChangePassword,
)

# User
from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
)

# Department
from .department import (
    DepartmentBase,
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
)

# Notice
from .notice import (
    NoticeBase,
    NoticeCreate,
    NoticeUpdate,
    NoticeResponse,
)

# Assignment
from .assignment import (
    AssignmentBase,
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
)

# Notification
from .notification import (
    NotificationBase,
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
    NotificationCount,
)

__all__ = [
    # Auth
    "UserLogin",
    "UserRegister",
    "Token",
    "ChangePassword",
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    # Department
    "DepartmentBase",
    "DepartmentCreate",
    "DepartmentUpdate",
    "DepartmentResponse",
    # Notice
    "NoticeBase",
    "NoticeCreate",
    "NoticeUpdate",
    "NoticeResponse",
    # Assignment
    "AssignmentBase",
    "AssignmentCreate",
    "AssignmentUpdate",
    "AssignmentResponse",
    # Notification
    "NotificationBase",
    "NotificationCreate",
    "NotificationUpdate",
    "NotificationResponse",
    "NotificationCount",
]