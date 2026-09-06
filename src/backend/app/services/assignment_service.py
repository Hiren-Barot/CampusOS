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

    def create_assignment(
        self,
        assignment_data: AssignmentCreate,
        faculty_id: int
    ) -> Assignment:
        assignment = self.assignment_repo.create(
            **assignment_data.model_dump(),
            faculty_id=faculty_id,
        )

        students = self.user_repo.get_students_by_department(
            assignment_data.department_id
        )
        for student in students:
            self.notification_service.create_notification(
                user_id=student.id,
                title=f"New Assignment: {assignment_data.title}",
                message=f"Due: {assignment_data.deadline.strftime('%Y-%m-%d %H:%M')}",
                type="assignment",
                related_id=assignment.id,
            )

        return assignment

    def get_assignment(self, assignment_id: int) -> Optional[Assignment]:
        return self.assignment_repo.get(assignment_id)

    def get_all_assignments(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Assignment]:
        return self.assignment_repo.get_all(skip=skip, limit=limit)

    def get_assignments_by_department(self, department_id: int) -> List[Assignment]:
        return self.assignment_repo.get_by_department(department_id)

    def get_assignments_by_faculty(self, faculty_id: int) -> List[Assignment]:
        return self.assignment_repo.get_by_faculty(faculty_id)

    def get_upcoming_assignments(
        self,
        department_id: Optional[int] = None
    ) -> List[Assignment]:
        return self.assignment_repo.get_upcoming(department_id)

    def get_expired_assignments(
        self,
        department_id: Optional[int] = None
    ) -> List[Assignment]:
        return self.assignment_repo.get_expired(department_id)

    def get_recent_assignments(self, limit: int = 10) -> List[Assignment]:
        return self.assignment_repo.get_recent(limit)

    def update_assignment(
        self,
        assignment_id: int,
        assignment_data: AssignmentUpdate
    ) -> Optional[Assignment]:
        update_data = assignment_data.model_dump(exclude_unset=True)
        return self.assignment_repo.update(assignment_id, **update_data)

    def delete_assignment(self, assignment_id: int) -> bool:
        return self.assignment_repo.delete(assignment_id)

    def search_assignments(self, query: str) -> List[Assignment]:
        return self.assignment_repo.search_assignments(query)

    def get_department_assignments_with_author(
        self,
        department_id: int
    ) -> List[dict]:
        assignments = self.assignment_repo.get_by_department(department_id)
        result = []

        for assignment in assignments:
            faculty = self.user_repo.get(assignment.faculty_id)
            result.append({
                "id": assignment.id,
                "title": assignment.title,
                "description": assignment.description,
                "deadline": assignment.deadline,
                "created_at": assignment.created_at,
                "updated_at": assignment.updated_at,
                "faculty_id": assignment.faculty_id,
                "faculty_name": faculty.full_name if faculty else "Unknown",
            })

        return result

    def can_edit_assignment(self, assignment_id: int, user_id: int) -> bool:
        assignment = self.assignment_repo.get(assignment_id)
        if not assignment:
            return False

        user = self.user_repo.get(user_id)
        if not user:
            return False

        if user.role == "admin":
            return True

        if user.role == "principal":
            return True

        if user.role == "hod" and user.department_id == assignment.department_id:
            return True

        if user.role == "faculty" and user.id == assignment.faculty_id:
            return True

        return False

    def can_delete_assignment(self, assignment_id: int, user_id: int) -> bool:
        return self.can_edit_assignment(assignment_id, user_id)