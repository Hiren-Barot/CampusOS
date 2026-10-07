from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from datetime import datetime, date
from sqlalchemy import String, Integer, Date, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from .user_model import User


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    enrollment_no: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True, index=True)
    course: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    semester: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    admission_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    parent_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    parent_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    qualification: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    specialization: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    experience_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    joining_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    designation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="profile")