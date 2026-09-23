from playwright.sync_api import Page, expect


class LoginPage:

    URL_PATH = "/login"

    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("#error-message")
        self.login_form = page.locator("#login-form")

    def navigate(self):
        self.page.goto(f"{self.base_url}{self.URL_PATH}")

    def fill_username(self, username):
        self.username_input.fill(username)

    def fill_password(self, password):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def login(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def get_error_text(self):
        if self.error_message.is_visible():
            return self.error_message.inner_text()
        return ""

    def expect_error_visible(self):
        expect(self.error_message).to_be_visible()

    def expect_error_contains(self, text):
        expect(self.error_message).to_contain_text(text)

    def expect_on_login_page(self):
        expect(self.login_form).to_be_visible()

    def expect_redirected_to_dashboard(self):
        self.page.wait_for_url("**/dashboard")
        expect(self.page).to_have_url(f"{self.base_url}/dashboard")
