# ============================================
# CAMPUSOS - NOTIFICATION MODEL
# ============================================
"""
Notification model for in-app notifications.
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


class Notification(Base):
    """
    Notification table for user notifications.
    """
    __tablename__ = "notifications"

    # ========================================
    # COLUMNS
    # ========================================
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # notice, assignment, deadline, system
    related_id: Mapped[Optional[int]] = mapped_column(nullable=True)  # notice_id or assignment_id
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    # ========================================
    # TIMESTAMPS
    # ========================================
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # ========================================
    # RELATIONSHIPS
    # ========================================
    # User who receives this notification
    user: Mapped["User"] = relationship(
        "User",
        back_populates="notifications"
    )