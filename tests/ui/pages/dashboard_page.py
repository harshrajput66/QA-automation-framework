"""
Dashboard Page — Page Object Model.

Encapsulates all locators and actions for the main dashboard page.
"""
from pathlib import Path

from playwright.sync_api import Page, expect


class DashboardPage:
    """Page Object for the dashboard at /dashboard."""

    URL_PATH = "/dashboard"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        # Navbar
        self.username_display = page.locator("#nav-username")
        self.logout_button = page.locator("#logout-button")

        # Upload section
        self.file_input = page.locator("#file-input")
        self.upload_button = page.locator("#upload-button")
        self.upload_message = page.locator("#upload-message")

        # Validation section
        self.validate_button = page.locator("#validate-button")
        self.validation_message = page.locator("#validation-message")

        # Results section
        self.results_section = page.locator("#results-section")
        self.summary_row = page.locator("#summary-row")
        self.results_table = page.locator("#results-table")
        self.results_body = page.locator("#results-body")

        # Report section
        self.report_button = page.locator("#report-button")
        self.download_button = page.locator("#download-button")
        self.report_message = page.locator("#report-message")

    def navigate(self):
        """Navigate to the dashboard."""
        self.page.goto(f"{self.base_url}{self.URL_PATH}")

    # ------------------------------------------------------------------
    # Upload actions
    # ------------------------------------------------------------------
    def upload_file(self, file_path: str):
        """Upload a file via the file input."""
        self.file_input.set_input_files(file_path)
        self.upload_button.click()

    def expect_upload_success(self):
        """Assert upload success message is displayed."""
        expect(self.upload_message).to_contain_text("uploaded successfully")

    def expect_upload_error(self):
        """Assert upload error message is displayed."""
        expect(self.upload_message).to_contain_text("❌")

    # ------------------------------------------------------------------
    # Validation actions
    # ------------------------------------------------------------------
    def start_validation(self):
        """Click the Start Validation button."""
        self.validate_button.click()

    def wait_for_validation_complete(self, timeout=30000):
        """Wait for validation to complete (message changes)."""
        expect(self.validation_message).to_contain_text("Validation completed", timeout=timeout)

    def expect_validation_results_visible(self):
        """Assert the results section is visible after validation."""
        expect(self.results_section).to_be_visible()

    def get_result_rows(self):
        """Return all result table row elements."""
        return self.results_body.locator("tr")

    def get_result_count(self) -> int:
        """Return the number of result rows in the table."""
        return self.get_result_rows().count()

    # ------------------------------------------------------------------
    # Report actions
    # ------------------------------------------------------------------
    def generate_report(self):
        """Click the Generate Report button."""
        self.report_button.click()

    def expect_report_success(self):
        """Assert report generation success message."""
        expect(self.report_message).to_contain_text("Reports generated successfully")

    def expect_download_button_visible(self):
        """Assert the Download Report button is visible."""
        expect(self.download_button).to_be_visible()

    def download_report(self):
        """Click the Download Report button and return the download."""
        with self.page.expect_download() as download_info:
            self.download_button.click()
        return download_info.value

    # ------------------------------------------------------------------
    # Logout
    # ------------------------------------------------------------------
    def logout(self):
        """Click the Logout button."""
        self.logout_button.click()

    def expect_on_dashboard(self):
        """Assert we are on the dashboard page."""
        expect(self.page).to_have_url(f"{self.base_url}/dashboard")
        expect(self.logout_button).to_be_visible()

    def expect_username_displayed(self, username: str):
        """Assert the username is displayed in the navbar."""
        expect(self.username_display).to_contain_text(username)
