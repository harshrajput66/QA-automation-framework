"""
Login Page — Page Object Model.

Encapsulates all locators and actions for the login page.
"""
from playwright.sync_api import Page, expect


class LoginPage:
    """Page Object for the login page at /login."""

    # Locators
    URL_PATH = "/login"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("#error-message")
        self.login_form = page.locator("#login-form")

    def navigate(self):
        """Navigate to the login page."""
        self.page.goto(f"{self.base_url}{self.URL_PATH}")

    def fill_username(self, username: str):
        """Fill in the username field."""
        self.username_input.fill(username)

    def fill_password(self, password: str):
        """Fill in the password field."""
        self.password_input.fill(password)

    def click_login(self):
        """Click the Sign In button."""
        self.login_button.click()

    def login(self, username: str, password: str):
        """Complete login flow: fill credentials and submit."""
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def get_error_text(self) -> str:
        """Return the error message text, if visible."""
        if self.error_message.is_visible():
            return self.error_message.inner_text()
        return ""

    def expect_error_visible(self):
        """Assert the error message is visible."""
        expect(self.error_message).to_be_visible()

    def expect_error_contains(self, text: str):
        """Assert the error message contains specific text."""
        expect(self.error_message).to_contain_text(text)

    def expect_on_login_page(self):
        """Assert we are on the login page."""
        expect(self.login_form).to_be_visible()

    def expect_redirected_to_dashboard(self):
        """Assert we were redirected to the dashboard."""
        self.page.wait_for_url("**/dashboard")
        expect(self.page).to_have_url(f"{self.base_url}/dashboard")
