# ============================================
# CAMPUSOS - NOTICE MODEL
# ============================================
"""
Notice model for department announcements.
Using SQLAlchemy 2.0 Mapped style with type hints.
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Text, Boolean, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# ============================================
# TYPE CHECKING IMPORTS (Lazy loading)
# ============================================
if TYPE_CHECKING:
    from .user_model import User
    from .department_model import Department


class Notice(Base):
    """
    Notice table for department announcements.
    """
    __tablename__ = "notices"

    # ========================================
    # COLUMNS
    # ========================================
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)

    # ========================================
    # TIMESTAMPS
    # ========================================
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    # ========================================
    # RELATIONSHIPS
    # ========================================
    # Department this notice belongs to
    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="notices"
    )

    # Faculty who created this notice
    faculty: Mapped["User"] = relationship(
        "User",
        back_populates="notices"
    )