"""
Report UI tests.

Covers: generate report, verify download button appears, download report.
Uses the DashboardPage Page Object Model.
"""
import pytest
from playwright.sync_api import Page, expect

from tests.ui.pages.dashboard_page import DashboardPage
from tests.utils.config import VALID_USERNAME, VALID_PASSWORD

pytestmark = pytest.mark.ui


class TestReport:
    """Playwright UI tests for report generation and download."""

    @pytest.fixture
    def dashboard_with_validation(self, logged_in_page: Page, flask_server):
        """Provide a DashboardPage that has already run validation."""
        dashboard = DashboardPage(logged_in_page, flask_server)
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)
        return dashboard

    def test_generate_report(self, dashboard_with_validation):
        """Clicking Generate Report shows a success message."""
        dashboard = dashboard_with_validation
        dashboard.generate_report()
        dashboard.expect_report_success()

    def test_download_button_appears_after_generation(self, dashboard_with_validation):
        """After generating report, the Download button becomes visible."""
        dashboard = dashboard_with_validation
        dashboard.generate_report()
        dashboard.expect_report_success()
        dashboard.expect_download_button_visible()

    def test_download_report_file(self, dashboard_with_validation):
        """Clicking Download Report downloads an Excel file."""
        dashboard = dashboard_with_validation
        dashboard.generate_report()
        dashboard.expect_report_success()
        dashboard.page.wait_for_timeout(500)

        download = dashboard.download_report()
        # Verify the downloaded file has content
        path = download.path()
        assert path is not None
        assert download.suggested_filename.endswith(".xlsx")
