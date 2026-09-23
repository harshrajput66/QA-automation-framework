import pytest

from tests.utils.config import VALID_USERNAME, VALID_PASSWORD

pytestmark = pytest.mark.api


class TestValidationAPI:

    @pytest.fixture(autouse=True)
    def _login(self, api_client):
        api_client.login(VALID_USERNAME, VALID_PASSWORD)

    def test_start_validation(self, api_client):
        resp = api_client.start_validation()
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "Validation completed"
        assert data["status"] == "completed"
        assert isinstance(data["total_tests"], int)
        assert data["total_tests"] > 0
        assert data["passed"] + data["failed"] == data["total_tests"]

    def test_get_status_after_validation(self, api_client):
        api_client.start_validation()
        resp = api_client.get_status()
        assert resp.status_code == 200
        data = resp.json()
        assert data["validated"] is True
        assert data["csv_exists"] is True
        assert data["db_exists"] is True

    def test_get_results_after_validation(self, api_client):
        api_client.start_validation()
        resp = api_client.get_results()
        assert resp.status_code == 200
        data = resp.json()
        assert "results" in data
        assert isinstance(data["results"], list)
        assert len(data["results"]) > 0

        for result in data["results"]:
            assert "test_id" in result
            assert "test_name" in result
            assert "status" in result
            assert result["status"] in ("PASS", "FAIL")

    def test_get_results_before_validation(self, api_client):
        from tests.api.api_client import APIClient
        fresh_client = APIClient(base_url=api_client.base_url)
        fresh_client.login(VALID_USERNAME, VALID_PASSWORD)
        resp = fresh_client.get_results()
        assert resp.status_code in (200, 400)

    def test_validation_results_contain_sql_checks(self, api_client):
        api_client.start_validation()
        resp = api_client.get_results()
        data = resp.json()
        sql_ids = [r["test_id"] for r in data["results"] if r["test_id"].startswith("TC-SQL")]
        assert len(sql_ids) == 7

    def test_validation_results_contain_pandas_checks(self, api_client):
        api_client.start_validation()
        resp = api_client.get_results()
        data = resp.json()
        pd_ids = [r["test_id"] for r in data["results"] if r["test_id"].startswith("TC-PD")]
        assert len(pd_ids) == 6
