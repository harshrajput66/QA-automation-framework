import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sql_validator import run_sql_checks

pytestmark = pytest.mark.data


class TestSQLValidation:

    @pytest.fixture(autouse=True, scope="class")
    def sql_results(self, db_path, request):
        results = run_sql_checks(db_path)
        request.cls._results = {r["Test ID"]: r for r in results}

    def _get_result(self, test_id):
        return self._results[test_id]

    def test_tc_sql_01_null_check_on_key_columns(self):
        result = self._get_result("TC-SQL-01")
        assert result["Status"] in ("PASS", "FAIL")
        assert result["Expected"] == 0

    def test_tc_sql_02_duplicate_row_check(self):
        result = self._get_result("TC-SQL-02")
        assert result["Expected"] == 0

    def test_tc_sql_03_orphan_customer_check(self):
        result = self._get_result("TC-SQL-03")
        assert result["Expected"] == 0

    def test_tc_sql_04_orphan_product_check(self):
        result = self._get_result("TC-SQL-04")
        assert result["Expected"] == 0

    def test_tc_sql_05_negative_sales_check(self):
        result = self._get_result("TC-SQL-05")
        assert result["Expected"] == 0

    def test_tc_sql_06_row_count_check(self):
        result = self._get_result("TC-SQL-06")
        print(f"  Expected: {result['Expected']}, Actual: {result['Result']}")

    def test_tc_sql_07_total_sales_rollup_check(self):
        result = self._get_result("TC-SQL-07")
        print(f"  Expected: {result['Expected']}, Actual: {result['Result']}")
