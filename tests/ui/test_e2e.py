"""
End-to-End UI test.

Complete workflow:
  Login → Upload CSV → Start Validation → Verify Results → Generate Report → Download → Logout
"""
import pytest
from playwright.sync_api import Page, expect

from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.dashboard_page import DashboardPage
from tests.utils.config import VALID_USERNAME, VALID_PASSWORD
from tests.utils.test_data import create_valid_test_csv

pytestmark = [pytest.mark.ui, pytest.mark.e2e]


class TestEndToEnd:
    """Complete end-to-end workflow test."""

    def test_full_qa_workflow(self, page: Page, flask_server, test_files):
        """
        E2E: Login → Upload → Validate → View Results → Generate Report → Download → Logout.

        This test exercises the complete user journey through the application.
        """
        # ----- Step 1: Login -----
        login_page = LoginPage(page, flask_server)
        login_page.navigate()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        login_page.expect_redirected_to_dashboard()

        # ----- Step 2: Verify Dashboard -----
        dashboard = DashboardPage(page, flask_server)
        dashboard.expect_on_dashboard()
        dashboard.expect_username_displayed(VALID_USERNAME)

        # ----- Step 3: Upload CSV -----
        csv_path = create_valid_test_csv(test_files)
        dashboard.upload_file(str(csv_path))
        dashboard.expect_upload_success()

        # ----- Step 4: Run Validation -----
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)

        # ----- Step 5: Verify Results -----
        dashboard.expect_validation_results_visible()
        page.wait_for_timeout(1000)
        row_count = dashboard.get_result_count()
        assert row_count > 0, "Expected validation results in the table"

        # Verify summary shows counts
        expect(dashboard.summary_row).to_be_visible()

        # ----- Step 6: Generate Report -----
        dashboard.generate_report()
        dashboard.expect_report_success()

        # ----- Step 7: Download Report -----
        dashboard.expect_download_button_visible()
        download = dashboard.download_report()
        assert download.suggested_filename.endswith(".xlsx")

        # ----- Step 8: Logout -----
        dashboard.logout()
        # Should be redirected back to login
        page.wait_for_url("**/login")
        expect(page).to_have_url(f"{flask_server}/login")
