import pytest
from fastapi.testclient import TestClient
from app.core.security.jwt import decode_token


class TestAuth:

    def test_register_student_success(self, client: TestClient, test_department):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newstudent@test.com",
                "password": "Student@123",
                "full_name": "New Student",
            },
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["must_change_password"] is False
        
        token = data["access_token"]
        payload = decode_token(token)
        assert payload is not None
        assert payload["role"] == "student"

    def test_register_student_duplicate_email(self, client: TestClient, test_student):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "student@test.com", 
                "password": "Student@123",
                "full_name": "Another Student",
            },
        )
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_register_student_invalid_email(self, client: TestClient):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "Student@123",
                "full_name": "Invalid Student",
            },
        )
        
        assert response.status_code == 422  

    def test_register_student_short_password(self, client: TestClient):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "weak@test.com",
                "password": "123",  
                "full_name": "Weak Password",
            },
        )
        
        assert response.status_code == 422  

    def test_login_success(self, client: TestClient, test_student):

        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
        token = data["access_token"]
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == str(test_student.id)

    def test_login_wrong_password(self, client: TestClient, test_student):
      
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "WrongPassword",
            },
        )
        
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self, client: TestClient):

        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@test.com",
                "password": "Password@123",
            },
        )
        
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_get_current_user(self, client: TestClient, test_student):
       
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]
        
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "student@test.com"
        assert data["full_name"] == "Test Student"
        assert data["role"] == "student"

    def test_get_current_user_invalid_token(self, client: TestClient):

        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"},
        )
        
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_get_current_user_no_token(self, client: TestClient):
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 403
        assert "not authenticated" in response.json()["detail"].lower()

    def test_change_password_success(self, client: TestClient, test_student):

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/v1/auth/change-password",
            json={
                "current_password": "Student@123",
                "new_password": "NewPass@123",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        assert "changed successfully" in response.json()["message"].lower()
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "NewPass@123",
            },
        )
        assert login_response.status_code == 200

    def test_change_password_wrong_current(self, client: TestClient, test_student):

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/v1/auth/change-password",
            json={
                "current_password": "WrongPassword",
                "new_password": "NewPass@123",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    def test_change_password_short_new(self, client: TestClient, test_student):

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/v1/auth/change-password",
            json={
                "current_password": "Student@123",
                "new_password": "123",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 422  

    def test_user_can_only_see_own_profile(self, client: TestClient, test_student, test_faculty):
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]
        
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "student@test.com"
        assert data["role"] == "student"
        assert data["id"] == test_student.id
        assert data["id"] != test_faculty.id