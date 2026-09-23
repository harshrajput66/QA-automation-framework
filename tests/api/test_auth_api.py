"""
Authentication API tests.

Covers: valid login, invalid login, missing credentials, logout.
"""
import pytest

from tests.utils.config import VALID_USERNAME, VALID_PASSWORD, INVALID_USERNAME, INVALID_PASSWORD

pytestmark = pytest.mark.api


class TestAuthAPI:
    """Authentication endpoint tests."""

    def test_login_valid_credentials(self, api_client):
        """POST /api/login with valid credentials returns 200."""
        resp = api_client.login(VALID_USERNAME, VALID_PASSWORD)
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "Login successful"
        assert data["username"] == VALID_USERNAME

    def test_login_invalid_credentials(self, api_client):
        """POST /api/login with wrong password returns 401."""
        resp = api_client.login(VALID_USERNAME, INVALID_PASSWORD)
        assert resp.status_code == 401
        data = resp.json()
        assert "error" in data
        assert "Invalid credentials" in data["error"]

    def test_login_invalid_username(self, api_client):
        """POST /api/login with wrong username returns 401."""
        resp = api_client.login(INVALID_USERNAME, VALID_PASSWORD)
        assert resp.status_code == 401

    def test_login_missing_username(self, api_client):
        """POST /api/login with empty username returns 400."""
        resp = api_client.login("", VALID_PASSWORD)
        assert resp.status_code == 400
        data = resp.json()
        assert "error" in data

    def test_login_missing_password(self, api_client):
        """POST /api/login with empty password returns 400."""
        resp = api_client.login(VALID_USERNAME, "")
        assert resp.status_code == 400

    def test_login_missing_both(self, api_client):
        """POST /api/login with no credentials returns 400."""
        resp = api_client.login("", "")
        assert resp.status_code == 400

    def test_logout(self, api_client):
        """POST /api/logout clears the session."""
        # Login first
        api_client.login(VALID_USERNAME, VALID_PASSWORD)
        # Logout
        resp = api_client.logout()
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "Logged out successfully"

    def test_access_protected_endpoint_without_login(self, api_client):
        """GET /api/status without login returns 401."""
        # Use a fresh client (no session cookies)
        from tests.api.api_client import APIClient
        fresh_client = APIClient(base_url=api_client.base_url)
        resp = fresh_client.get_status()
        assert resp.status_code == 401
