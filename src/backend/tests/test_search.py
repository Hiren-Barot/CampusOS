# ============================================
# CAMPOS - SEARCH TESTS
# ============================================
"""
Tests for unified search endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestSearch:
    """Test unified search endpoints."""

    def test_search_all_as_student(self, client: TestClient, test_student, test_notice, test_assignment):
        """Test student can search all content."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/search/?q=test",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        
        # Should have notices and assignments (not users or departments)
        assert "notices" in data
        assert "assignments" in data
        assert "users" not in data
        assert "departments" not in data
        
        # Should contain the test notice and assignment
        notice_titles = [n["title"] for n in data["notices"]]
        assert "Test Notice" in notice_titles
        
        assignment_titles = [a["title"] for a in data["assignments"]]
        assert "Test Assignment" in assignment_titles

    def test_search_notices_only(self, client: TestClient, test_student, test_notice):
        """Test student can search notices only."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/search/?q=test&type=notices",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        
        assert "notices" in data
        assert "assignments" not in data
        
        notice_titles = [n["title"] for n in data["notices"]]
        assert "Test Notice" in notice_titles

    def test_search_assignments_only(self, client: TestClient, test_student, test_assignment):
        """Test student can search assignments only."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/search/?q=test&type=assignments",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        
        assert "assignments" in data
        assert "notices" not in data
        
        assignment_titles = [a["title"] for a in data["assignments"]]
        assert "Test Assignment" in assignment_titles

    def test_search_users_as_admin(self, client: TestClient, test_admin, test_student):
        """Test admin can search users."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/search/?q=student&type=users",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        
        assert "users" in data
        user_emails = [u["email"] for u in data["users"]]
        assert "student@test.com" in user_emails

    def test_search_users_as_student_forbidden(self, client: TestClient, test_student):
        """Test student cannot search users."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/search/?q=admin&type=users",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 400
        assert "don't have permission" in response.json()["detail"].lower()

    def test_search_departments_as_admin(self, client: TestClient, test_admin, test_department):
        """Test admin can search departments."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/search/?q=computer&type=departments",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        
        assert "departments" in data
        dept_names = [d["name"] for d in data["departments"]]
        assert "Computer Engineering" in dept_names

    def test_search_departments_as_student_forbidden(self, client: TestClient, test_student):
        """Test student cannot search departments."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/search/?q=computer&type=departments",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 400
        assert "don't have permission" in response.json()["detail"].lower()

    def test_search_with_department_filter(self, client: TestClient, test_admin, test_department):
        """Test search with department filter."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            f"/api/v1/search/?q=test&department_id={test_department.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        
        # Should only return results from the specified department
        for notice in data.get("notices", []):
            assert notice["department_id"] == test_department.id
        
        for assignment in data.get("assignments", []):
            assert assignment["department_id"] == test_department.id

    def test_search_limit_parameter(self, client: TestClient, test_admin):
        """Test search with limit parameter."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "Admin@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/search/?q=test&limit=1",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        
        # Each category should have at most 1 result
        for key, value in data.items():
            if isinstance(value, list):
                assert len(value) <= 1

    def test_search_no_results(self, client: TestClient, test_student):
        """Test search with no matching results."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/search/?q=nonexistent123456",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        
        # Should have empty lists but still exist
        assert "notices" in data
        assert "assignments" in data
        assert len(data["notices"]) == 0
        assert len(data["assignments"]) == 0