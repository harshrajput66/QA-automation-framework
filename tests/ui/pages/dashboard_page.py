from playwright.sync_api import Page, expect


class DashboardPage:

    URL_PATH = "/dashboard"

    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

        self.username_display = page.locator("#nav-username")
        self.logout_button = page.locator("#logout-button")

        self.file_input = page.locator("#file-input")
        self.upload_button = page.locator("#upload-button")
        self.upload_message = page.locator("#upload-message")

        self.validate_button = page.locator("#validate-button")
        self.validation_message = page.locator("#validation-message")

        self.results_section = page.locator("#results-section")
        self.summary_row = page.locator("#summary-row")
        self.results_table = page.locator("#results-table")
        self.results_body = page.locator("#results-body")

        self.report_button = page.locator("#report-button")
        self.download_button = page.locator("#download-button")
        self.report_message = page.locator("#report-message")

    def navigate(self):
        self.page.goto(f"{self.base_url}{self.URL_PATH}")

    def upload_file(self, file_path):
        self.file_input.set_input_files(file_path)
        self.upload_button.click()

    def expect_upload_success(self):
        expect(self.upload_message).to_contain_text("uploaded successfully")

    def expect_upload_error(self):
        expect(self.upload_message).to_contain_text("❌")

    def start_validation(self):
        self.validate_button.click()

    def wait_for_validation_complete(self, timeout=30000):
        expect(self.validation_message).to_contain_text("Validation completed", timeout=timeout)

    def expect_validation_results_visible(self):
        expect(self.results_section).to_be_visible()

    def get_result_rows(self):
        return self.results_body.locator("tr")

    def get_result_count(self):
        return self.get_result_rows().count()

    def generate_report(self):
        self.report_button.click()

    def expect_report_success(self):
        expect(self.report_message).to_contain_text("Reports generated successfully")

    def expect_download_button_visible(self):
        expect(self.download_button).to_be_visible()

    def download_report(self):
        with self.page.expect_download() as download_info:
            self.download_button.click()
        return download_info.value

    def logout(self):
        self.logout_button.click()

    def expect_on_dashboard(self):
        expect(self.page).to_have_url(f"{self.base_url}/dashboard")
        expect(self.logout_button).to_be_visible()

    def expect_username_displayed(self, username):
        expect(self.username_display).to_contain_text(username)
