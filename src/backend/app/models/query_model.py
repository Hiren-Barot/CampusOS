from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from .user_model import User
    from .department_model import Department


class Query(Base):

    __tablename__ = "queries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)

    reply: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    replied_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    replied_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    student: Mapped["User"] = relationship(
        "User",
        foreign_keys=[student_id],
        back_populates="queries_asked",
    )

    replied_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[replied_by_id],
    )

    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="queries",
    )