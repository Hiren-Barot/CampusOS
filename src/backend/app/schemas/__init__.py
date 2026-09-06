from .auth_schemas import (
    UserLogin,
    UserRegister,
    Token,
    ChangePassword,
)

from .user_schemas import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
)

from .department_schemas import (
    DepartmentBase,
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
)

from .notice_schemas import (
    NoticeBase,
    NoticeCreate,
    NoticeUpdate,
    NoticeResponse,
)

from .assignment_schemas import (
    AssignmentBase,
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
)

from .notification_schemas import (
    NotificationBase,
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
    NotificationCount,
)

__all__ = [
    "UserLogin",
    "UserRegister",
    "Token",
    "ChangePassword",

    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",

    "DepartmentBase",
    "DepartmentCreate",
    "DepartmentUpdate",
    "DepartmentResponse",

    "NoticeBase",
    "NoticeCreate",
    "NoticeUpdate",
    "NoticeResponse",

    "AssignmentBase",
    "AssignmentCreate",
    "AssignmentUpdate",
    "AssignmentResponse",
    
    "NotificationBase",
    "NotificationCreate",
    "NotificationUpdate",
    "NotificationResponse",
    "NotificationCount",
]