import pytest
from playwright.sync_api import Page

from tests.utils.config import VALID_USERNAME, VALID_PASSWORD, SCREENSHOT_ON_FAILURE


@pytest.fixture
def logged_in_page(page, flask_server):
    page.goto(f"{flask_server}/login")
    page.fill("#username", VALID_USERNAME)
    page.fill("#password", VALID_PASSWORD)
    page.click("#login-button")
    page.wait_for_url(f"**/dashboard")
    return page


@pytest.fixture(autouse=True)
def _screenshot_on_failure(request, page):
    yield
    if SCREENSHOT_ON_FAILURE and request.node.rep_call and request.node.rep_call.failed:
        screenshot_path = f"test-results/{request.node.name}.png"
        page.screenshot(path=screenshot_path)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
