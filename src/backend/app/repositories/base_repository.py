from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get(self, id: int) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_all(self,skip: int = 0,limit: int = 100,**filters) -> List[ModelType]:
        stmt = select(self.model)

        for key, value in filters.items():
            if value is not None:
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)

        stmt = stmt.offset(skip).limit(limit)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        instance = self.get(id)
        if not instance:
            return None

        for key, value in kwargs.items():
            if value is not None:
                if hasattr(instance, key):
                    setattr(instance, key, value)

        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        instance = self.get(id)
        if not instance:
            return False

        self.db.delete(instance)
        self.db.commit()
        return True

    def count(self, **filters) -> int:
        stmt = select(self.model)

        for key, value in filters.items():
            if value is not None:
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)

        result = self.db.execute(stmt)
        return len(result.scalars().all())