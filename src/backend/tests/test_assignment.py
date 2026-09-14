import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta


class TestAssignments:

    def test_get_all_assignments_as_student(self, client: TestClient, test_student, test_assignment):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/assignments/",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        titles = [a["title"] for a in data]
        assert "Test Assignment" in titles

    def test_create_assignment_as_faculty(self, client: TestClient, test_faculty, test_department):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        token = login_response.json()["access_token"]

        deadline = (datetime.now() + timedelta(days=7)).isoformat()

        response = client.post(
            "/api/v1/assignments/",
            json={
                "title": "New Assignment",
                "description": "This is a new assignment.",
                "department_id": test_department.id,
                "deadline": deadline,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Assignment"
        assert data["description"] == "This is a new assignment."
        assert data["department_id"] == test_department.id

    def test_create_assignment_as_student_forbidden(self, client: TestClient, test_student, test_department):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        deadline = (datetime.now() + timedelta(days=7)).isoformat()

        response = client.post(
            "/api/v1/assignments/",
            json={
                "title": "Student Assignment",
                "description": "Students cannot create assignments.",
                "department_id": test_department.id,
                "deadline": deadline,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403
        assert "not allowed" in response.json()["detail"].lower()

    def test_get_assignment_by_id(self, client: TestClient, test_student, test_assignment):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/assignments/{test_assignment.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_assignment.id
        assert data["title"] == "Test Assignment"

    def test_get_assignment_not_found(self, client: TestClient, test_student):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/assignments/9999",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_own_assignment_as_faculty(self, client: TestClient, test_faculty, test_assignment):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.put(
            f"/api/v1/assignments/{test_assignment.id}",
            json={
                "title": "Updated Assignment Title",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Assignment Title"

    def test_update_other_assignment_as_faculty_forbidden(self, client: TestClient, test_faculty, test_hod, test_department):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "hod@test.com",
                "password": "HOD@123",
            },
        )
        hod_token = login_response.json()["access_token"]

        deadline = (datetime.now() + timedelta(days=7)).isoformat()

        assign_response = client.post(
            "/api/v1/assignments/",
            json={
                "title": "HOD Assignment",
                "description": "This is HOD's assignment.",
                "department_id": test_department.id,
                "deadline": deadline,
            },
            headers={"Authorization": f"Bearer {hod_token}"},
        )
        hod_assignment_id = assign_response.json()["id"]

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        faculty_token = login_response.json()["access_token"]

        response = client.put(
            f"/api/v1/assignments/{hod_assignment_id}",
            json={
                "title": "Faculty Tried to Change",
            },
            headers={"Authorization": f"Bearer {faculty_token}"},
        )

        assert response.status_code == 403
        assert "don't have permission" in response.json()["detail"].lower()

    def test_delete_own_assignment_as_faculty(self, client: TestClient, test_faculty, test_assignment):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.delete(
            f"/api/v1/assignments/{test_assignment.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()

    def test_get_upcoming_assignments(self, client: TestClient, test_student, test_assignment):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/assignments/upcoming",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 0  

    def test_search_assignments_as_student(self, client: TestClient, test_student, test_assignment):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/assignments/search?q=test",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        titles = [a["title"] for a in data]
        assert "Test Assignment" in titles

    def test_student_cannot_access_other_dept_assignment(
        self, 
        client: TestClient, 
        test_student, 
        test_department,
        test_admin
    ):
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_admin.email,  
                "password": "Admin@123",
            },
        )
        admin_token = login_response.json()["access_token"]

        dept_response = client.post(
            "/api/v1/departments/",
            json={
                "name": "Other Department",
                "code": "OD",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        other_dept_id = dept_response.json()["id"]

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_student.email,
                "password": "Student@123",
            },
        )
        student_token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/assignments/?department_id={other_dept_id}",
            headers={"Authorization": f"Bearer {student_token}"},
        )

        assert response.status_code == 403