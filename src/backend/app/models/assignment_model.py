# ============================================
# CAMPUSOS - ASSIGNMENT MODEL
# ============================================
"""
Assignment model for student assignments.
Using SQLAlchemy 2.0 Mapped style with type hints.
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# ============================================
# TYPE CHECKING IMPORTS (Lazy loading)
# ============================================
if TYPE_CHECKING:
    from .user_model import User
    from .department_model import Department


class Assignment(Base):
    """
    Assignment table for academic assignments.
    """
    __tablename__ = "assignments"

    # ========================================
    # COLUMNS
    # ========================================
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    deadline: Mapped[datetime] = mapped_column(nullable=False)

    # ========================================
    # TIMESTAMPS
    # ========================================
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    # ========================================
    # RELATIONSHIPS
    # ========================================
    # Department this assignment belongs to
    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="assignments"
    )

    # Faculty who created this assignment
    faculty: Mapped["User"] = relationship(
        "User",
        back_populates="assignments"
    )