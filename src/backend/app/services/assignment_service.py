from typing import Optional, List
from sqlalchemy.orm import Session

from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.assignment_schemas import AssignmentCreate, AssignmentUpdate
from app.models.assignment_model import Assignment
from app.services.notification_service import NotificationService


class AssignmentService:

    def __init__(self, db: Session):
        self.db = db
        self.assignment_repo = AssignmentRepository(db)
        self.user_repo = UserRepository(db)
        self.notification_service = NotificationService(db)

    def _enrich(self, a: Assignment) -> dict:
        faculty = self.user_repo.get(a.faculty_id)
        return {
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "department_id": a.department_id,
            "faculty_id": a.faculty_id,
            "faculty_name": faculty.full_name if faculty else "Unknown",
            "deadline": a.deadline,
            "created_at": a.created_at,
            "updated_at": a.updated_at,
        }

    def create_assignment(self, assignment_data: AssignmentCreate, faculty_id: int) -> dict:
        assignment = self.assignment_repo.create(
            title=assignment_data.title,
            description=assignment_data.description,
            department_id=assignment_data.department_id,
            deadline=assignment_data.deadline,
            faculty_id=faculty_id,
        )

        if assignment_data.department_id:
            students = self.user_repo.get_students_by_department(assignment_data.department_id)
            for student in students:
                self.notification_service.create_notification(
                    user_id=student.id,
                    title=f"New Assignment: {assignment.title}",
                    message=f"Due: {assignment.deadline.strftime('%Y-%m-%d %H:%M')}",
                    type="assignment",
                    related_id=assignment.id,
                )

        return self._enrich(assignment)

    def get_assignment(self, assignment_id: int) -> Optional[dict]:
        a = self.assignment_repo.get(assignment_id)
        return self._enrich(a) if a else None

    def get_all_assignments(self, skip: int = 0, limit: int = 100):
        assignments = self.assignment_repo.get_all(skip=skip, limit=limit)
        return [self._enrich(a) for a in assignments]

    def get_assignments_by_department(self, department_id: int):
        assignments = self.assignment_repo.get_by_department(department_id)
        return [self._enrich(a) for a in assignments]

    def get_assignments_by_faculty(self, faculty_id: int):
        assignments = self.assignment_repo.get_by_faculty(faculty_id)
        return [self._enrich(a) for a in assignments]

    def get_upcoming_assignments(self, department_id=None):
        assignments = self.assignment_repo.get_upcoming(department_id)
        return [self._enrich(a) for a in assignments]

    def get_expired_assignments(self, department_id=None):
        assignments = self.assignment_repo.get_expired(department_id)
        return [self._enrich(a) for a in assignments]

    def get_recent_assignments(self, limit: int = 10):
        assignments = self.assignment_repo.get_recent(limit)
        return [self._enrich(a) for a in assignments]

    def update_assignment(self, assignment_id: int, data: AssignmentUpdate):
        update_data = data.model_dump(exclude_unset=True)
        a = self.assignment_repo.update(assignment_id, **update_data)
        return self._enrich(a) if a else None

    def delete_assignment(self, assignment_id: int) -> bool:
        return self.assignment_repo.delete(assignment_id)

    def search_assignments(self, query: str):
        assignments = self.assignment_repo.search_assignments(query)
        return [self._enrich(a) for a in assignments]