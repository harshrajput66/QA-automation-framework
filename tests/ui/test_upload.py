import pytest
from playwright.sync_api import Page

from tests.ui.pages.dashboard_page import DashboardPage
from tests.utils.test_data import create_valid_test_csv, create_non_csv_file

pytestmark = pytest.mark.ui


class TestUpload:

    @pytest.fixture
    def dashboard(self, logged_in_page, flask_server):
        return DashboardPage(logged_in_page, flask_server)

    def test_upload_valid_csv(self, dashboard, test_files):
        csv_path = create_valid_test_csv(test_files)
        dashboard.upload_file(str(csv_path))
        dashboard.expect_upload_success()

    def test_upload_non_csv_file(self, dashboard, test_files):
        txt_path = create_non_csv_file(test_files)
        dashboard.upload_file(str(txt_path))
        dashboard.expect_upload_error()
