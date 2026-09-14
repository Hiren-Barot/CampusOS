from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user_model import User
    from app.models.notice_model import Notice
    from app.models.assignment_model import Assignment


class Department(Base):

    __tablename__ = 'departments'
   
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hod_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", use_alter=True, name="fk_departments_hod_id"),
        nullable=True
    )    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    
    users: Mapped[List["User"]] = relationship(
        "User",
        back_populates="department",
        foreign_keys="User.department_id"
    )
    
    notices: Mapped[List["Notice"]] = relationship(
        "Notice",
        back_populates="department"
    )
    
    assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment",
        back_populates="department"
    )
    
    hod: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[hod_id],
        uselist=False
    )