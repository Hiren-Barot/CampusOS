# ============================================
# CAMPOS - USER MODEL
# ============================================
"""
User model with role-based access control and profile information.
Using SQLAlchemy 2.0 Mapped style with type hints.
"""

from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, date
from sqlalchemy import String, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# ============================================
# TYPE CHECKING IMPORTS (Lazy loading)
# ============================================
if TYPE_CHECKING:
    from backend.app.models.department_model import Department
    from src.backend.app.models.notice import Notice
    from src.backend.app.models.assignment import Assignment
    from src.backend.app.models.notification import Notification


class User(Base):
    """
    User table storing all user accounts with profile information.
    """
    __tablename__ = "users"

    # ========================================
    # AUTHENTICATION (Primary)
    # ========================================
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="student")
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)

    # ========================================
    # ACCOUNT STATUS
    # ========================================
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    must_change_password: Mapped[bool] = mapped_column(Boolean, default=True)

    # ========================================
    # PROFILE INFORMATION
    # ========================================
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(nullable=True)
    profile_picture: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # ========================================
    # TIMESTAMPS
    # ========================================
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    # ========================================
    # RELATIONSHIPS
    # ========================================
    # Department this user belongs to
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        back_populates="users"
    )
    
    # Notices created by this user (if Faculty/HOD/Principal)
    notices: Mapped[List["Notice"]] = relationship(
        "Notice",
        back_populates="faculty"
    )
    
    # Assignments created by this user (if Faculty/HOD/Principal)
    assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment",
        back_populates="faculty"
    )
    
    # Notifications for this user
    notifications: Mapped[List["Notification"]] = relationship(
        "Notification",
        back_populates="user"
    )