import pytest
from playwright.sync_api import Page, expect

from tests.ui.pages.login_page import LoginPage
from tests.utils.config import VALID_USERNAME, VALID_PASSWORD, INVALID_PASSWORD

pytestmark = pytest.mark.ui


class TestLogin:

    @pytest.fixture
    def login_page(self, page, flask_server):
        lp = LoginPage(page, flask_server)
        lp.navigate()
        return lp

    def test_login_page_loads(self, login_page):
        login_page.expect_on_login_page()
        expect(login_page.username_input).to_be_visible()
        expect(login_page.password_input).to_be_visible()
        expect(login_page.login_button).to_be_visible()

    def test_login_page_title(self, login_page):
        expect(login_page.page).to_have_title("Login — Data QA Framework")

    def test_valid_login_redirects_to_dashboard(self, login_page):
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        login_page.expect_redirected_to_dashboard()

    def test_invalid_password_shows_error(self, login_page):
        login_page.login(VALID_USERNAME, INVALID_PASSWORD)
        login_page.expect_error_visible()
        login_page.expect_error_contains("Invalid credentials")

    def test_invalid_username_shows_error(self, login_page):
        login_page.login("nonexistent_user", VALID_PASSWORD)
        login_page.expect_error_visible()
        login_page.expect_error_contains("Invalid credentials")

    def test_empty_username_shows_error(self, login_page):
        login_page.login("", VALID_PASSWORD)
        login_page.expect_error_visible()

    def test_empty_password_shows_error(self, login_page):
        login_page.login(VALID_USERNAME, "")
        login_page.expect_error_visible()

    def test_empty_both_fields_shows_error(self, login_page):
        login_page.login("", "")
        login_page.expect_error_visible()
