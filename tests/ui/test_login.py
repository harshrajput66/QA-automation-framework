"""
Login UI tests.

Covers: valid login, invalid login, empty credentials.
Uses the LoginPage Page Object Model.
"""
import pytest
from playwright.sync_api import Page, expect

from tests.ui.pages.login_page import LoginPage
from tests.utils.config import VALID_USERNAME, VALID_PASSWORD, INVALID_PASSWORD

pytestmark = pytest.mark.ui


class TestLogin:
    """Playwright UI tests for the login page."""

    @pytest.fixture
    def login_page(self, page: Page, flask_server):
        """Provide a LoginPage object navigated to the login URL."""
        lp = LoginPage(page, flask_server)
        lp.navigate()
        return lp

    def test_login_page_loads(self, login_page):
        """Login page renders with username/password fields and button."""
        login_page.expect_on_login_page()
        expect(login_page.username_input).to_be_visible()
        expect(login_page.password_input).to_be_visible()
        expect(login_page.login_button).to_be_visible()

    def test_login_page_title(self, login_page):
        """Login page has the correct title."""
        expect(login_page.page).to_have_title("Login — Data QA Framework")

    def test_valid_login_redirects_to_dashboard(self, login_page):
        """Valid credentials redirect to the dashboard."""
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        login_page.expect_redirected_to_dashboard()

    def test_invalid_password_shows_error(self, login_page):
        """Invalid password shows an error message on the login page."""
        login_page.login(VALID_USERNAME, INVALID_PASSWORD)
        login_page.expect_error_visible()
        login_page.expect_error_contains("Invalid credentials")

    def test_invalid_username_shows_error(self, login_page):
        """Invalid username shows an error message."""
        login_page.login("nonexistent_user", VALID_PASSWORD)
        login_page.expect_error_visible()
        login_page.expect_error_contains("Invalid credentials")

    def test_empty_username_shows_error(self, login_page):
        """Empty username shows a validation error."""
        login_page.login("", VALID_PASSWORD)
        login_page.expect_error_visible()

    def test_empty_password_shows_error(self, login_page):
        """Empty password shows a validation error."""
        login_page.login(VALID_USERNAME, "")
        login_page.expect_error_visible()

    def test_empty_both_fields_shows_error(self, login_page):
        """Empty username and password shows a validation error."""
        login_page.login("", "")
        login_page.expect_error_visible()
