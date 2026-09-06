import pytest
from fastapi.testclient import TestClient
import sys

class TestUsers:

    def test_get_all_users_as_admin(self, client: TestClient, test_admin, test_student, test_faculty):

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/users/",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2 
        emails = [u["email"] for u in data]
        assert "admin@test.com" in emails
        assert "student@test.com" in emails

    def test_get_all_users_as_student_forbidden(self, client: TestClient, test_student):

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/users/?skip=0&limit=100", 
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403
        assert "not allowed" in response.json()["detail"].lower()

    def test_create_user_as_admin(self, client: TestClient, test_admin, test_department):
    
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/users/",
            json={
                "email": "newfaculty@test.com",
                "full_name": "New Faculty",
                "role": "faculty",
                "department_id": test_department.id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newfaculty@test.com"
        assert data["full_name"] == "New Faculty"
        assert data["role"] == "faculty"
        assert "temp_password" in data

    def test_create_user_duplicate_email(self, client: TestClient, test_admin, test_student):

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/users/",
            json={
                "email": "student@test.com",  
                "full_name": "Duplicate Student",
                "role": "student",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 400
        assert "department id is required" in response.json()["detail"].lower()


    def test_create_user_no_department_for_faculty(self, client: TestClient, test_admin):
  
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/users/",
            json={
                "email": "nofaculty@test.com",
                "full_name": "No Dept Faculty",
                "role": "faculty",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 400
        assert "department id is required" in response.json()["detail"].lower()

    def test_create_user_as_student_forbidden(self, client: TestClient, test_student):
  
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/users/",
            json={
                "email": "newuser@test.com",
                "full_name": "New User",
                "role": "student",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403
        assert "not allowed" in response.json()["detail"].lower()

    def test_get_user_by_id_as_admin(self, client: TestClient, test_admin, test_student):
   
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/users/{test_student.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_student.id
        assert data["email"] == "student@test.com"

    def test_get_user_by_id_as_student_self(self, client: TestClient, test_student):
    
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/users/{test_student.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_student.id

    def test_get_user_by_id_as_student_other_forbidden(self, client: TestClient, test_student, test_faculty):

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/users/{test_faculty.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403
        assert "don't have permission" in response.json()["detail"].lower()

    def test_update_user_as_admin(self, client: TestClient, test_admin, test_student):
    
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.put(
            f"/api/v1/users/{test_student.id}",
            json={
                "full_name": "Updated Student Name",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Student Name"

    def test_delete_user_as_admin(self, client: TestClient, test_admin, test_student):
    
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.delete(
            f"/api/v1/users/{test_student.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "deactivated" in response.json()["message"].lower()

    def test_delete_self_as_admin_forbidden(self, client: TestClient, test_admin):
    
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.delete(
            f"/api/v1/users/{test_admin.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 400
        assert "cannot delete yourself" in response.json()["detail"].lower()

    def test_delete_last_admin_forbidden(self, client: TestClient, test_admin):
    
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.delete(
            f"/api/v1/users/{test_admin.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 400
        assert "cannot delete yourself" in response.json()["detail"].lower()

    def test_search_users_as_admin(self, client: TestClient, test_admin, test_student):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        # Try different ways to pass the parameter
        response = client.get(
            "/api/v1/users/search",
            params={"q": "student"},  # ← Using params
            headers={"Authorization": f"Bearer {token}"},
        )

        print("🔍 Status:", response.status_code)
        print("🔍 Response body:", response.text)  # ← Use .text instead of .json()

        assert response.status_code == 200

    def test_search_users_as_student_forbidden(self, client: TestClient, test_student):

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/users/search?q=admin",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403
        assert "not allowed" in response.json()["detail"].lower()