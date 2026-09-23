import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from pandas_reconciler import run_pandas_checks

pytestmark = pytest.mark.data


class TestPandasValidation:

    @pytest.fixture(autouse=True, scope="class")
    def pandas_results(self, source_df, target_df, request):
        results = run_pandas_checks(source=source_df, target=target_df)
        request.cls._results = {r["Test ID"]: r for r in results}

    def _get_result(self, test_id):
        return self._results[test_id]

    def test_tc_pd_01_column_names_check(self):
        result = self._get_result("TC-PD-01")
        assert result["Expected"] == 0

    def test_tc_pd_02_row_count_check(self):
        result = self._get_result("TC-PD-02")
        print(f"  Expected: {result['Expected']}, Actual: {result['Result']}")

    def test_tc_pd_03_null_value_check(self):
        result = self._get_result("TC-PD-03")
        assert result["Expected"] == 0

    def test_tc_pd_04_duplicate_row_check(self):
        result = self._get_result("TC-PD-04")
        assert result["Expected"] == 0

    def test_tc_pd_05_cell_level_value_diff(self):
        result = self._get_result("TC-PD-05")
        assert result["Expected"] == 0

    def test_tc_pd_06_numeric_tolerance_check(self):
        result = self._get_result("TC-PD-06")
        assert result["Expected"] == 0
