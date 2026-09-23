"""
Validation UI tests.

Covers: start validation, verify results displayed, verify PASS/FAIL counts.
Uses the DashboardPage Page Object Model.
"""
import pytest
from playwright.sync_api import Page, expect

from tests.ui.pages.dashboard_page import DashboardPage
from tests.utils.config import VALID_USERNAME, VALID_PASSWORD

pytestmark = pytest.mark.ui


class TestValidation:
    """Playwright UI tests for the validation workflow."""

    @pytest.fixture
    def dashboard(self, logged_in_page: Page, flask_server):
        """Provide a DashboardPage object (already logged in)."""
        return DashboardPage(logged_in_page, flask_server)

    def test_start_validation(self, dashboard):
        """Clicking Start Validation runs the pipeline and shows completion."""
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)

    def test_results_section_visible_after_validation(self, dashboard):
        """After validation, the results section becomes visible."""
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)
        dashboard.expect_validation_results_visible()

    def test_results_table_populated(self, dashboard):
        """After validation, the results table has rows."""
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)
        # Wait for table to be populated
        dashboard.page.wait_for_timeout(1000)
        row_count = dashboard.get_result_count()
        assert row_count == 13, f"Expected 13 result rows (7 SQL + 6 Pandas), got {row_count}"

    def test_results_contain_pass_and_fail(self, dashboard):
        """Results table contains both PASS and FAIL statuses."""
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)
        dashboard.page.wait_for_timeout(1000)
        pass_cells = dashboard.results_body.locator(".status-pass")
        fail_cells = dashboard.results_body.locator(".status-fail")
        assert pass_cells.count() > 0, "Expected at least one PASS result"
        assert fail_cells.count() > 0, "Expected at least one FAIL result (demo defects)"

    def test_summary_counts_displayed(self, dashboard):
        """Summary row shows Total, Passed, Failed counts."""
        dashboard.start_validation()
        dashboard.wait_for_validation_complete(timeout=30000)
        dashboard.page.wait_for_timeout(1000)
        expect(dashboard.summary_row).to_be_visible()
        summary_text = dashboard.summary_row.inner_text()
        assert "Total" in summary_text
        assert "Passed" in summary_text
        assert "Failed" in summary_text
