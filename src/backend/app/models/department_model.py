# ============================================
# CAMPOS - DEPARTMENT MODEL
# ============================================
"""
Department model representing academic departments.
Using SQLAlchemy 2.0 Mapped style with type hints.
"""
from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from src.backend.app.models.user_model import User
    from src.backend.app.models.notice_model import Notice
    from src.backend.app.models.assignment_model import Assignment


class Department(Base):
    """
    Department table for academic departments.
    """
    __tablename__ = "departments"

    # ========================================
    # COLUMNS
    # ========================================
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hod_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    # ========================================
    # TIMESTAMPS
    # ========================================
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # ========================================
    # RELATIONSHIPS
    # ========================================
    # Users belonging to this department (students + faculty + HOD)
    users: Mapped[List["User"]] = relationship(
        "User",
        back_populates="department"
    )
    
    # Notices posted in this department
    notices: Mapped[List["Notice"]] = relationship(
        "Notice",
        back_populates="department"
    )
    
    # Assignments posted in this department
    assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment",
        back_populates="department"
    )
    
    # HOD user (one-to-one relationship)
    hod: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[hod_id],
        uselist=False
    )