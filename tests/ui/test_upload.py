"""
Upload UI tests.

Covers: valid CSV upload, invalid file type, UI feedback messages.
Uses the DashboardPage Page Object Model.
"""
import pytest
from playwright.sync_api import Page

from tests.ui.pages.dashboard_page import DashboardPage
from tests.utils.config import VALID_USERNAME, VALID_PASSWORD
from tests.utils.test_data import create_valid_test_csv, create_non_csv_file

pytestmark = pytest.mark.ui


class TestUpload:
    """Playwright UI tests for file upload functionality."""

    @pytest.fixture
    def dashboard(self, logged_in_page: Page, flask_server):
        """Provide a DashboardPage object (already logged in)."""
        return DashboardPage(logged_in_page, flask_server)

    def test_upload_valid_csv(self, dashboard, test_files):
        """Uploading a valid CSV shows a success message."""
        csv_path = create_valid_test_csv(test_files)
        dashboard.upload_file(str(csv_path))
        dashboard.expect_upload_success()

    def test_upload_non_csv_file(self, dashboard, test_files):
        """Uploading a non-CSV file shows an error message."""
        txt_path = create_non_csv_file(test_files)
        dashboard.upload_file(str(txt_path))
        dashboard.expect_upload_error()
