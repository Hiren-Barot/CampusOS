from typing import Optional, List
from datetime import datetime , timezone
from sqlalchemy.orm import Session

from app.repositories.query_repository import QueryRepository
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import DepartmentRepository
from app.schemas.query_schemas import QueryCreate, QueryReply
from app.models.query_model import Query
from app.services.notification_service import NotificationService


class QueryService:

    def __init__(self, db: Session):
        self.db = db
        self.query_repo = QueryRepository(db)
        self.user_repo = UserRepository(db)
        self.dept_repo = DepartmentRepository(db)
        self.notification_service = NotificationService(db)

    def _enrich(self, q: Query) -> dict:
        student = self.user_repo.get(q.student_id)
        replier = self.user_repo.get(q.replied_by_id) if q.replied_by_id else None
        dept = self.dept_repo.get(q.department_id)

        return {
            "id": q.id,
            "title": q.title,
            "description": q.description,
            "student_id": q.student_id,
            "student_name": student.full_name if student else "Unknown",
            "department_id": q.department_id,
            "department_name": dept.name if dept else None,
            "reply": q.reply,
            "replied_by_id": q.replied_by_id,
            "replied_by_name": replier.full_name if replier else None,
            "replied_at": q.replied_at,
            "status": q.status,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
        }

    def create_query(self, data: QueryCreate, student_id: int) -> dict:
        student = self.user_repo.get(student_id)
        if not student:
            raise ValueError("Student not found")
        if not student.department_id:
            raise ValueError("You have no department assigned")

        query = self.query_repo.create(
            title=data.title,
            description=data.description,
            student_id=student_id,
            department_id=student.department_id,
            status="open",
        )

        self._notify_dept_staff(query)

        return self._enrich(query)

    def _notify_dept_staff(self, query: Query):
        faculty = self.user_repo.get_faculty_by_department(query.department_id)
        staff_ids = [f.id for f in faculty if f.id != query.student_id]

        dept = self.dept_repo.get(query.department_id)
        if dept and dept.hod_id and dept.hod_id not in staff_ids:
            staff_ids.append(dept.hod_id)

        for uid in staff_ids:
            self.notification_service.create_notification(
                user_id=uid,
                title=f"New Query: {query.title}",
                message=query.description[:120] + ("..." if len(query.description) > 120 else ""),
                type="query",
                related_id=query.id,
            )

    def reply_to_query(self, query_id: int, data: QueryReply, replier_id: int) -> Optional[dict]:
        query = self.query_repo.get(query_id)
        if not query:
            return None
        if query.status == "answered":
            raise ValueError("Query has already been answered")

        replier = self.user_repo.get(replier_id)
        if not replier:
            raise ValueError("Replier not found")

        if replier.role in ["faculty", "hod"]:
            if replier.department_id != query.department_id:
                raise PermissionError("You can only reply to queries in your department")

        updated = self.query_repo.update(
            query_id,
            reply=data.reply,
            replied_by_id=replier_id,
            replied_at=datetime.now(timezone.utc),
            status="answered",
        )

        self.notification_service.create_notification(
            user_id=query.student_id,
            title=f"Query Answered: {query.title}",
            message=data.reply[:120] + ("..." if len(data.reply) > 120 else ""),
            type="query_reply",
            related_id=query.id,
        )

        return self._enrich(updated) if updated else None

    def get_query(self, query_id: int) -> Optional[dict]:
        q = self.query_repo.get(query_id)
        return self._enrich(q) if q else None

    def get_queries_for_user(self, user) -> List[dict]:
        if user.role == "student":
            queries = self.query_repo.get_by_student(user.id)
        elif user.role in ["faculty", "hod"]:
            if not user.department_id:
                return []
            queries = self.query_repo.get_by_department(user.department_id)
        elif user.role in ["admin", "principal"]:
            queries = self.query_repo.get_all_ordered()
        else:
            queries = []
        return [self._enrich(q) for q in queries]

    def delete_query(self, query_id: int, user_id: int) -> bool:
        query = self.query_repo.get(query_id)
        if not query:
            return False
        if query.student_id != user_id:
            raise PermissionError("You can only delete your own queries")
        if query.status == "answered":
            raise ValueError("Cannot delete an answered query")
        return self.query_repo.delete(query_id)

    def can_view_query(self, query: dict, user) -> bool:
        if user.role in ["admin", "principal"]:
            return True
        if user.role == "student":
            return query["student_id"] == user.id
        if user.role in ["faculty", "hod"]:
            return query["department_id"] == user.department_id
        return False