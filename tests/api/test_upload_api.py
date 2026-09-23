"""
Upload API tests.

Covers: valid CSV upload, invalid file type, missing file, unauthorized upload.
"""
import pytest

from tests.utils.config import VALID_USERNAME, VALID_PASSWORD
from tests.utils.test_data import (
    create_valid_test_csv,
    create_non_csv_file,
)

pytestmark = pytest.mark.api


class TestUploadAPI:
    """File upload endpoint tests."""

    @pytest.fixture(autouse=True)
    def _login(self, api_client):
        """Ensure authenticated before each test."""
        api_client.login(VALID_USERNAME, VALID_PASSWORD)

    def test_upload_valid_csv(self, api_client, test_files):
        """POST /api/upload with valid CSV returns 200."""
        csv_path = create_valid_test_csv(test_files)
        resp = api_client.upload_file(str(csv_path))
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "File uploaded successfully"
        assert "filename" in data
        assert "size" in data
        assert data["size"] > 0

    def test_upload_non_csv_file(self, api_client, test_files):
        """POST /api/upload with non-CSV file returns 400."""
        txt_path = create_non_csv_file(test_files)
        resp = api_client.upload_file_with_name(str(txt_path), "document.txt")
        assert resp.status_code == 400
        data = resp.json()
        assert "error" in data
        assert "CSV" in data["error"]

    def test_upload_no_file(self, api_client):
        """POST /api/upload with no file returns 400."""
        resp = api_client.session.post(
            f"{api_client.base_url}/api/upload",
            timeout=10,
        )
        assert resp.status_code == 400

    def test_upload_unauthorized(self, api_client):
        """POST /api/upload without login returns 401."""
        from tests.api.api_client import APIClient
        fresh_client = APIClient(base_url=api_client.base_url)
        resp = fresh_client.session.post(
            f"{fresh_client.base_url}/api/upload",
            timeout=10,
        )
        assert resp.status_code == 401
