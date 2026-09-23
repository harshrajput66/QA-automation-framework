import pytest

from tests.utils.config import VALID_USERNAME, VALID_PASSWORD

pytestmark = pytest.mark.api


class TestReportAPI:

    @pytest.fixture(autouse=True)
    def _login_and_validate(self, api_client):
        api_client.login(VALID_USERNAME, VALID_PASSWORD)
        api_client.start_validation()

    def test_generate_report(self, api_client):
        resp = api_client.generate_report()
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "Reports generated successfully"
        assert "report_path" in data
        assert "test_case_path" in data

    def test_download_report(self, api_client):
        api_client.generate_report()
        resp = api_client.download_report()
        assert resp.status_code == 200
        assert len(resp.content) > 100

    def test_download_report_before_generation(self, api_client):
        from tests.api.api_client import APIClient
        fresh_client = APIClient(base_url=api_client.base_url)
        fresh_client.login(VALID_USERNAME, VALID_PASSWORD)
        resp = fresh_client.download_report()
        assert resp.status_code in (200, 400)

    def test_generate_report_without_validation(self, api_client):
        from tests.api.api_client import APIClient
        fresh_client = APIClient(base_url=api_client.base_url)
        fresh_client.login(VALID_USERNAME, VALID_PASSWORD)
        resp = fresh_client.generate_report()
        assert resp.status_code in (200, 400)
