import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"

CSV_PATH = DATA_DIR / "kaggle_sales_raw.csv"
DB_PATH = DATA_DIR / "target_dwh.db"
REPORT_PATH = PROJECT_ROOT / "QA_Test_Execution_Report.xlsx"
TEST_CASE_PATH = PROJECT_ROOT / "TestCases.xlsx"

sys.path.insert(0, str(SRC_DIR))

from excel_reporter import generate_excel_report
from kaggle_loader import run_etl
from pandas_reconciler import run_pandas_checks
from sql_validator import run_sql_checks
from test_case_writer import generate_test_cases_excel


def print_step(number, title):
    print(f"\nSTEP {number}: {title}")
    print("-" * 60)


def ensure_csv_exists():
    if CSV_PATH.exists():
        print(f"Dataset found: {CSV_PATH}")
        return

    print("Dataset not found, so sample data will be generated.")
    print("Real dataset: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final")

    from generate_sample_data import create_sample_csv

    create_sample_csv(output_path=str(CSV_PATH), n_rows=1000)


def print_final_summary(sql_results, pandas_results, report_path, test_case_path):
    all_results = sql_results + pandas_results
    total_tests = len(all_results)
    passed_tests = sum(1 for result in all_results if result["Status"] == "PASS")
    failed_tests = sum(1 for result in all_results if result["Status"] == "FAIL")

    print("\n" + "=" * 60)
    print("QA RUN COMPLETE")
    print(f"Total Tests : {total_tests}")
    print(f"Passed      : {passed_tests}")
    print(f"Failed      : {failed_tests} (expected, because demo defects are injected)")
    print(f"QA Report   : {report_path}")
    print(f"Test Cases  : {test_case_path}")
    print("=" * 60)


def main():
    print("=" * 60)
    print("Data QA Framework - Source to Target Reconciliation")
    print("Tools: Python, Pandas, NumPy, SQLite, OpenPyXL")
    print("=" * 60)

    ensure_csv_exists()

    print_step(1, "Build source and target tables")
    tables = run_etl(str(CSV_PATH), str(DB_PATH))

    print_step(2, "Run SQL validation checks")
    sql_results = run_sql_checks(str(DB_PATH))

    print_step(3, "Run Pandas and NumPy checks")
    pandas_results = run_pandas_checks(
        source=tables["fact_source"],
        target=tables["fact_target"],
    )

    print_step(4, "Create Excel QA report")
    report_path = generate_excel_report(sql_results, pandas_results, output_path=str(REPORT_PATH))

    print_step(5, "Create Excel test case document")
    test_case_path = generate_test_cases_excel(sql_results, pandas_results, output_path=str(TEST_CASE_PATH))

    print_final_summary(sql_results, pandas_results, report_path, test_case_path)


if __name__ == "__main__":
    main()
