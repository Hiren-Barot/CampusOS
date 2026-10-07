from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from .department_model import Department
    from .notice_model import Notice
    from .assignment_model import Assignment
    from .notification_model import Notification
    from .profile_model import Profile


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="student")
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    must_change_password: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        back_populates="users",
        foreign_keys=[department_id],
    )
    notices: Mapped[List["Notice"]] = relationship("Notice", back_populates="faculty")
    assignments: Mapped[List["Assignment"]] = relationship("Assignment", back_populates="faculty")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user")

    profile: Mapped[Optional["Profile"]] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )