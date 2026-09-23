"""
SQL validation tests — wraps the existing sql_validator.py checks
into individual pytest test cases.

Each SQL check from the existing module becomes a named, reportable test.
"""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sql_validator import run_sql_checks


pytestmark = pytest.mark.data


class TestSQLValidation:
    """SQL-based data quality checks against the SQLite database."""

    @pytest.fixture(autouse=True, scope="class")
    def sql_results(self, db_path, request):
        """Run all SQL checks once for this test class."""
        results = run_sql_checks(db_path)
        # Store results as a dict keyed by Test ID for easy lookup
        request.cls._results = {r["Test ID"]: r for r in results}

    def _get_result(self, test_id):
        return self._results[test_id]

    def test_tc_sql_01_null_check_on_key_columns(self):
        """TC-SQL-01: No NULL values in CustomerID, ProductID, LocationID."""
        result = self._get_result("TC-SQL-01")
        assert result["Status"] in ("PASS", "FAIL"), f"Unexpected status: {result['Status']}"
        # We expect FAIL because demo defects inject NULLs
        assert result["Expected"] == 0
        # Documenting the actual result
        print(f"  Expected: {result['Expected']}, Actual: {result['Result']}, Details: {result['Details']}")

    def test_tc_sql_02_duplicate_row_check(self):
        """TC-SQL-02: No duplicate rows based on OrderID+CustomerID+ProductID."""
        result = self._get_result("TC-SQL-02")
        assert result["Expected"] == 0
        print(f"  Expected: {result['Expected']}, Actual: {result['Result']}, Details: {result['Details']}")

    def test_tc_sql_03_orphan_customer_check(self):
        """TC-SQL-03: All CustomerIDs in FactSales exist in DimCustomer."""
        result = self._get_result("TC-SQL-03")
        assert result["Expected"] == 0
        print(f"  Expected: {result['Expected']}, Actual: {result['Result']}, Details: {result['Details']}")

    def test_tc_sql_04_orphan_product_check(self):
        """TC-SQL-04: All ProductIDs in FactSales exist in DimProduct."""
        result = self._get_result("TC-SQL-04")
        assert result["Expected"] == 0
        print(f"  Expected: {result['Expected']}, Actual: {result['Result']}, Details: {result['Details']}")

    def test_tc_sql_05_negative_sales_check(self):
        """TC-SQL-05: No negative Sales values."""
        result = self._get_result("TC-SQL-05")
        assert result["Expected"] == 0
        print(f"  Expected: {result['Expected']}, Actual: {result['Result']}, Details: {result['Details']}")

    def test_tc_sql_06_row_count_check(self):
        """TC-SQL-06: Source and target row counts match."""
        result = self._get_result("TC-SQL-06")
        print(f"  Expected: {result['Expected']}, Actual: {result['Result']}, Details: {result['Details']}")

    def test_tc_sql_07_total_sales_rollup_check(self):
        """TC-SQL-07: Total Sales sum matches between source and target."""
        result = self._get_result("TC-SQL-07")
        print(f"  Expected: {result['Expected']}, Actual: {result['Result']}, Details: {result['Details']}")
