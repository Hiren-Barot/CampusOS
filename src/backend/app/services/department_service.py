from typing import Optional, List
from sqlalchemy.orm import Session

from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.department_schemas import DepartmentCreate, DepartmentUpdate
from app.models.department_model import Department


class DepartmentService:

    def __init__(self, db: Session):
        self.db = db
        self.dept_repo = DepartmentRepository(db)
        self.user_repo = UserRepository(db)

    def create_department(self, dept_data: DepartmentCreate) -> Optional[Department]:
        existing_dept = self.dept_repo.get_by_code(dept_data.code)
        if existing_dept:
            return None

        return self.dept_repo.create(**dept_data.model_dump())

    def get_department(self, dept_id: int) -> Optional[Department]:
        return self.dept_repo.get(dept_id)

    def get_department_by_code(self, code: str) -> Optional[Department]:
        return self.dept_repo.get_by_code(code)

    def get_all_departments(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Department]:
        return self.dept_repo.get_all(skip=skip, limit=limit)

    def update_department(
        self,
        dept_id: int,
        dept_data: DepartmentUpdate,
    ) -> Optional[Department]:
        
        update_data = dept_data.model_dump(exclude_unset=True)
        return self.dept_repo.update(dept_id, **update_data)

    def delete_department(self, dept_id: int) -> bool:
        return self.dept_repo.delete(dept_id)

    def assign_hod(self, dept_id: int, hod_id: int) -> Optional[Department]:
        dept = self.dept_repo.get(dept_id)
        if not dept:
            return None

        hod = self.user_repo.get(hod_id)
        if not hod:
            return None

        existing_hod_dept = self.dept_repo.get_all(hod_id=hod_id)
        if existing_hod_dept:
            for dept in existing_hod_dept:
                self.dept_repo.update(dept.id, hod_id=None)

        updated_dept = self.dept_repo.update(dept_id, hod_id=hod_id)
        return updated_dept

    def search_departments(self, query: str) -> List[Department]:
        return self.dept_repo.search_departments(query)

    def get_department_stats(self, dept_id: int) -> dict:
        dept = self.dept_repo.get(dept_id)
        if not dept:
            return {}

        faculty = self.user_repo.get_faculty_by_department(dept_id)
        students = self.user_repo.get_students_by_department(dept_id)

        return {
            "department_name": dept.name,
            "department_code": dept.code,
            "faculty_count": len(faculty),
            "student_count": len(students),
            "hod_id": dept.hod_id,
        }