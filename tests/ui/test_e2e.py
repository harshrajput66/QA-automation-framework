import pytest
from playwright.sync_api import Page, expect

from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.dashboard_page import DashboardPage
from tests.utils.config import VALID_USERNAME, VALID_PASSWORD
from tests.utils.test_data import create_valid_test_csv

pytestmark = [pytest.mark.ui, pytest.mark.e2e]


class TestEndToEnd:

    def test_full_qa_workflow(self, page, flask_server, test_files):
        login_page = LoginPage(page, flask_server)
        login_page.navigate()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        login_page.expect_redirected_to_dashboard()

        dashboard = DashboardPage(page, flask_server)
        dashboard.expect_on_dashboard()
        dashboard.expect_username_displayed(VALID_USERNAME)

        csv_path = create_valid_test_csv(test_files)
        dashboard.upload_file(str(csv_path))
        dashboard.expect_upload_success()

        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)

        dashboard.expect_validation_results_visible()
        page.wait_for_timeout(1000)
        row_count = dashboard.get_result_count()
        assert row_count > 0

        expect(dashboard.summary_row).to_be_visible()

        dashboard.generate_report()
        dashboard.expect_report_success()

        dashboard.expect_download_button_visible()
        download = dashboard.download_report()
        assert download.suggested_filename.endswith(".xlsx")

        dashboard.logout()
        page.wait_for_url("**/login")
        expect(page).to_have_url(f"{flask_server}/login")
