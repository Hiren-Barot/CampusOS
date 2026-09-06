import pytest
from fastapi.testclient import TestClient


class TestDepartments:

    def test_get_all_departments_as_student(self, client: TestClient, test_student):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/departments/",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        names = [d["name"] for d in data]
        assert "Computer Engineering" in names

    def test_create_department_as_admin(self, client: TestClient, test_admin):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/departments/",
            json={
                "name": "Data Science",
                "code": "DS",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Data Science"
        assert data["code"] == "DS"

    def test_create_department_duplicate_code(self, client: TestClient, test_admin, test_department):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/departments/",
            json={
                "name": "Computer Science",
                "code": "CE",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_create_department_as_student_forbidden(self, client: TestClient, test_student):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/departments/",
            json={
                "name": "New Department",
                "code": "ND",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403
        assert "not allowed" in response.json()["detail"].lower()

    def test_get_department_by_id(self, client: TestClient, test_student, test_department):
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/departments/{test_department.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_department.id
        assert data["name"] == "Computer Engineering"
        assert data["code"] == "CE"

    def test_get_department_not_found(self, client: TestClient, test_student):
       
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/departments/9999",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_department_as_admin(self, client: TestClient, test_admin, test_department):
       
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.put(
            f"/api/v1/departments/{test_department.id}",
            json={
                "name": "Updated Computer Engineering",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Computer Engineering"

    def test_delete_department_as_admin(self, client: TestClient, test_admin, test_department):
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.delete(
            f"/api/v1/departments/{test_department.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()

    def test_assign_hod_as_admin(self, client: TestClient, test_admin, test_department, test_faculty):
       
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.post(
            f"/api/v1/departments/{test_department.id}/hod/{test_faculty.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "hod assigned successfully" in response.json()["message"].lower()

        dept_response = client.get(
            f"/api/v1/departments/{test_department.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert dept_response.status_code == 200
        assert dept_response.json()["hod_id"] == test_faculty.id

    def test_remove_hod_as_admin(self, client: TestClient, test_admin, test_department, test_hod):

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        test_department.hod_id = test_hod.id

        response = client.delete(
            f"/api/v1/departments/{test_department.id}/hod",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "hod removed successfully" in response.json()["message"].lower()

    def test_get_department_stats_as_hod(self, client: TestClient, test_hod, test_department):
       
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "hod@test.com",
                "password": "HOD@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/departments/{test_department.id}/stats",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["department_name"] == "Computer Engineering"
        assert "faculty_count" in data
        assert "student_count" in data

    def test_get_department_stats_as_student_forbidden(self, client: TestClient, test_student, test_department):
       
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/departments/{test_department.id}/stats",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403
        assert "not allowed" in response.json()["detail"].lower()

    def test_search_departments(self, client: TestClient, test_student, test_department):
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/departments/search?q=computer",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        names = [d["name"] for d in data]
        assert "Computer Engineering" in names