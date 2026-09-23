import pytest
from playwright.sync_api import Page, expect

from tests.ui.pages.dashboard_page import DashboardPage

pytestmark = pytest.mark.ui


class TestReport:

    @pytest.fixture
    def dashboard_with_validation(self, logged_in_page, flask_server):
        dashboard = DashboardPage(logged_in_page, flask_server)
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)
        return dashboard

    def test_generate_report(self, dashboard_with_validation):
        dashboard = dashboard_with_validation
        dashboard.generate_report()
        dashboard.expect_report_success()

    def test_download_button_appears_after_generation(self, dashboard_with_validation):
        dashboard = dashboard_with_validation
        dashboard.generate_report()
        dashboard.expect_report_success()
        dashboard.expect_download_button_visible()

    def test_download_report_file(self, dashboard_with_validation):
        dashboard = dashboard_with_validation
        dashboard.generate_report()
        dashboard.expect_report_success()
        dashboard.page.wait_for_timeout(500)
        download = dashboard.download_report()
        path = download.path()
        assert path is not None
        assert download.suggested_filename.endswith(".xlsx")
