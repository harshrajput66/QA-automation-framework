import pytest
from playwright.sync_api import Page, expect

from tests.ui.pages.dashboard_page import DashboardPage

pytestmark = pytest.mark.ui


class TestValidation:

    @pytest.fixture
    def dashboard(self, logged_in_page, flask_server):
        return DashboardPage(logged_in_page, flask_server)

    def test_start_validation(self, dashboard):
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)

    def test_results_section_visible_after_validation(self, dashboard):
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)
        dashboard.expect_validation_results_visible()

    def test_results_table_populated(self, dashboard):
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)
        dashboard.page.wait_for_timeout(1000)
        row_count = dashboard.get_result_count()
        assert row_count == 13

    def test_results_contain_pass_and_fail(self, dashboard):
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)
        dashboard.page.wait_for_timeout(1000)
        pass_cells = dashboard.results_body.locator(".status-pass")
        fail_cells = dashboard.results_body.locator(".status-fail")
        assert pass_cells.count() > 0
        assert fail_cells.count() > 0

    def test_summary_counts_displayed(self, dashboard):
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)
        dashboard.page.wait_for_timeout(1000)
        expect(dashboard.summary_row).to_be_visible()
        summary_text = dashboard.summary_row.inner_text()
        assert "Total" in summary_text
        assert "Passed" in summary_text
        assert "Failed" in summary_text
