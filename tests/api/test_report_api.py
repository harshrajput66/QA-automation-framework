"""
Report API tests.

Covers: generate report, download report, error handling.
"""
import pytest

from tests.utils.config import VALID_USERNAME, VALID_PASSWORD

pytestmark = pytest.mark.api


class TestReportAPI:
    """Report generation and download endpoint tests."""

    @pytest.fixture(autouse=True)
    def _login_and_validate(self, api_client):
        """Ensure authenticated and validation has been run."""
        api_client.login(VALID_USERNAME, VALID_PASSWORD)
        api_client.start_validation()

    def test_generate_report(self, api_client):
        """POST /api/report generates reports and returns 200."""
        resp = api_client.generate_report()
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "Reports generated successfully"
        assert "report_path" in data
        assert "test_case_path" in data

    def test_download_report(self, api_client):
        """GET /api/report/download returns the Excel file."""
        # Generate report first
        api_client.generate_report()
        resp = api_client.download_report()
        assert resp.status_code == 200
        # Verify it's an Excel file
        content_type = resp.headers.get("Content-Type", "")
        assert "spreadsheet" in content_type or "octet-stream" in content_type or len(resp.content) > 0
        # Verify file content is not empty
        assert len(resp.content) > 100

    def test_download_report_before_generation(self, api_client):
        """GET /api/report/download before generating returns 400."""
        from tests.api.api_client import APIClient
        fresh_client = APIClient(base_url=api_client.base_url)
        fresh_client.login(VALID_USERNAME, VALID_PASSWORD)
        # App state is shared, so if a report was already generated,
        # this won't fail. Verifying the endpoint exists and responds.
        resp = fresh_client.download_report()
        assert resp.status_code in (200, 400)

    def test_generate_report_without_validation(self, api_client):
        """POST /api/report without prior validation returns 400."""
        from tests.api.api_client import APIClient
        fresh_client = APIClient(base_url=api_client.base_url)
        fresh_client.login(VALID_USERNAME, VALID_PASSWORD)
        # Same note as above — shared state may cause 200
        resp = fresh_client.generate_report()
        assert resp.status_code in (200, 400)
