# ============================================
# CAMPOS - NOTIFICATION TESTS
# ============================================
"""
Tests for notification management endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestNotifications:
    """Test notification management endpoints."""

    def test_get_notifications_as_student(self, client: TestClient, test_student):
        """Test student can get their notifications."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/notifications/",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        # Should be a list (may be empty initially)
        assert isinstance(data, list)

    def test_get_unread_count(self, client: TestClient, test_student):
        """Test student can get unread notification count."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/notifications/unread/count",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert isinstance(data["count"], int)

    def test_get_unread_notifications(self, client: TestClient, test_student):
        """Test student can get unread notifications."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/notifications/unread",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_mark_notification_as_read(self, client: TestClient, test_student, db_session):
        """Test student can mark a notification as read."""
        from app.services.notification_service import NotificationService
        
        # ✅ Use db_session from the test
        notification_service = NotificationService(db_session)
        
        notification = notification_service.create_notification(
            user_id=test_student.id,
            title="Test Notification",
            message="This is a test notification.",
            type="system",
        )
        # Don't close db_session! It's managed by the test fixture.

        # Login as student
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_student.email,  # ← USE FIXTURE EMAIL
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.patch(
            f"/api/v1/notifications/{notification.id}/read",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "marked as read" in response.json()["message"].lower()

    def test_mark_other_user_notification_forbidden(self, client: TestClient, test_student, test_faculty, db_session):
        from app.services.notification_service import NotificationService
        
        notification_service = NotificationService(db_session)
        
        notification = notification_service.create_notification(
            user_id=test_faculty.id,
            title="Test Notification",
            message="This is a test notification.",
            type="system",
        )

        # Login as student
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_student.email,
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.patch(
            f"/api/v1/notifications/{notification.id}/read",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403
        assert "only mark your own" in response.json()["detail"].lower()

    def test_mark_all_as_read(self, client: TestClient, test_student):
        """Test student can mark all notifications as read."""
        # Create some notifications for student
        from app.services.notification_service import NotificationService
        from app.core.database import SessionLocal
        
        db = SessionLocal()
        notification_service = NotificationService(db)
        
        for i in range(3):
            notification_service.create_notification(
                user_id=test_student.id,
                title=f"Test Notification {i}",
                message=f"This is test notification {i}.",
                type="system",
            )
        db.close()

        # Login as student
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@test.com",
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.patch(
            "/api/v1/notifications/read-all",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "notifications marked as read" in response.json()["message"].lower()

    def test_delete_notification(self, client: TestClient, test_student, db_session):
        from app.services.notification_service import NotificationService
        
        notification_service = NotificationService(db_session)
        
        notification = notification_service.create_notification(
            user_id=test_student.id,
            title="Test Notification",
            message="This is a test notification.",
            type="system",
        )

        # Login as student
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_student.email,
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.delete(
            f"/api/v1/notifications/{notification.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()

    def test_delete_other_user_notification_forbidden(self, client: TestClient, test_student, test_faculty, db_session):
        from app.services.notification_service import NotificationService
        
        notification_service = NotificationService(db_session)
        
        notification = notification_service.create_notification(
            user_id=test_faculty.id,
            title="Test Notification",
            message="This is a test notification.",
            type="system",
        )

        # Login as student
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_student.email,
                "password": "Student@123",
            },
        )
        token = login_response.json()["access_token"]

        response = client.delete(
            f"/api/v1/notifications/{notification.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403
        assert "only delete your own" in response.json()["detail"].lower()