from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from .user_model import User
    from .department_model import Department

class Assignment(Base):

    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    deadline: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())


    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="assignments"
    )

    faculty: Mapped["User"] = relationship(
        "User",
        back_populates="assignments"
    )