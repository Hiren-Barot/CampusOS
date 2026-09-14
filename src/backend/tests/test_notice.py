# ============================================
# CAMPOS - NOTICE TESTS
# ============================================
"""
Tests for notice management endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestNotices:
    """Test notice management endpoints."""

    def test_get_all_notices_as_student(self, client: TestClient, test_student, test_notice):
        """Test student can view all published notices in their department."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/notices/",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        titles = [n["title"] for n in data]
        assert "Test Notice" in titles

    def test_create_notice_as_faculty(self, client: TestClient, test_faculty, test_department):
        """Test faculty can create a notice."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/notices/",
            json={
                "title": "New Faculty Notice",
                "content": "This is a new notice from faculty.",
                "department_id": test_department.id,
                "is_published": True,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Faculty Notice"
        assert data["content"] == "This is a new notice from faculty."
        assert data["department_id"] == test_department.id
        assert data["is_published"] is True

    def test_create_notice_as_student_forbidden(self, client: TestClient, test_student, test_department):
        """Test student cannot create a notice."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/notices/",
            json={
                "title": "Student Notice",
                "content": "Students cannot create notices.",
                "department_id": test_department.id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403
        assert "not allowed" in response.json()["detail"].lower()

    def test_get_notice_by_id(self, client: TestClient, test_student, test_notice):
        """Test student can get a specific notice by ID."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/notices/{test_notice.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_notice.id
        assert data["title"] == "Test Notice"

    def test_get_notice_not_found(self, client: TestClient, test_student):
        """Test getting non-existent notice returns 404."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/notices/9999",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_own_notice_as_faculty(self, client: TestClient, test_faculty, test_notice):
        """Test faculty can update their own notice."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.put(
            f"/api/v1/notices/{test_notice.id}",
            json={
                "title": "Updated Notice Title",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Notice Title"

    def test_update_other_notice_as_faculty_forbidden(self, client: TestClient, test_faculty, test_hod, test_department):
        """Test faculty cannot update another faculty's notice."""
        # Create a notice by HOD
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "hod@test.com",
                "password": "HOD@123",
            },
        )
        hod_token = login_response.json()["access_token"]

        notice_response = client.post(
            "/api/v1/notices/",
            json={
                "title": "HOD Notice",
                "content": "This is HOD's notice.",
                "department_id": test_department.id,
            },
            headers={"Authorization": f"Bearer {hod_token}"},
        )
        hod_notice_id = notice_response.json()["id"]

        # Login as faculty
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        faculty_token = login_response.json()["access_token"]

        # Try to update HOD's notice
        response = client.put(
            f"/api/v1/notices/{hod_notice_id}",
            json={
                "title": "Faculty Tried to Change",
            },
            headers={"Authorization": f"Bearer {faculty_token}"},
        )

        assert response.status_code == 403
        assert "don't have permission" in response.json()["detail"].lower()

    def test_delete_own_notice_as_faculty(self, client: TestClient, test_faculty, test_notice):
        """Test faculty can delete their own notice."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.delete(
            f"/api/v1/notices/{test_notice.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()

    def test_publish_notice_as_faculty(self, client: TestClient, test_faculty, test_department):
        """Test faculty can publish a draft notice."""
        # Create draft notice
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        token = login_response.json()["access_token"]

        create_response = client.post(
            "/api/v1/notices/",
            json={
                "title": "Draft Notice",
                "content": "This is a draft notice.",
                "department_id": test_department.id,
                "is_published": False,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        notice_id = create_response.json()["id"]

        # Publish the notice
        response = client.patch(
            f"/api/v1/notices/{notice_id}/publish",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "published successfully" in response.json()["message"].lower()

    def test_unpublish_notice_as_faculty(self, client: TestClient, test_faculty, test_notice):
        """Test faculty can unpublish a notice."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.patch(
            f"/api/v1/notices/{test_notice.id}/unpublish",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "unpublished successfully" in response.json()["message"].lower()

    def test_search_notices_as_student(self, client: TestClient, test_student, test_notice):
        """Test student can search notices."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/notices/search?q=test",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        titles = [n["title"] for n in data]
        assert "Test Notice" in titles

    def test_student_cannot_see_unpublished_notice(self, client: TestClient, test_faculty, test_student, test_department):
        """Test student cannot see unpublished notices."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "faculty@test.com",
                "password": "Faculty@123",
            },
        )
        faculty_token = login_response.json()["access_token"]

        create_response = client.post(
            "/api/v1/notices/",
            json={
                "title": "Secret Draft",
                "content": "This is a secret draft.",
                "department_id": test_department.id,
                "is_published": False,
            },
            headers={"Authorization": f"Bearer {faculty_token}"},
        )
        draft_id = create_response.json()["id"]

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        student_token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/notices/{draft_id}",
            headers={"Authorization": f"Bearer {student_token}"},
        )

        assert response.status_code == 403
        assert "not published" in response.json()["detail"].lower()