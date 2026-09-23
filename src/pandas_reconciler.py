import numpy as np


CRITICAL_COLUMNS = ["OrderID", "CustomerID", "ProductID", "LocationID", "Sales"]
KEY_COLUMNS = ["OrderID", "CustomerID", "ProductID"]
MEASURE_COLUMNS = ["Sales", "Quantity", "Discount", "Profit"]


def make_result(test_id, test_name, expected, actual, details, extra_fields=None):
    result = {
        "Test ID": test_id,
        "Test Name": test_name,
        "Expected": expected,
        "Result": actual,
        "Status": "PASS" if expected == actual else "FAIL",
        "Details": details,
    }

    if extra_fields:
        result.update(extra_fields)

    return result


def run_pandas_checks(source, target):
    print("Running Pandas checks...")

    results = []

    source_columns = list(source.columns)
    target_columns = list(target.columns)
    columns_match = source_columns == target_columns

    results.append(
        make_result(
            "TC-PD-01",
            "Column Names Check",
            0,
            0 if columns_match else 1,
            "All columns match" if columns_match else "Source and target columns are different",
        )
    )

    source_rows = len(source)
    target_rows = len(target)
    row_difference = target_rows - source_rows

    results.append(
        make_result(
            "TC-PD-02",
            "Row Count Check",
            source_rows,
            target_rows,
            f"Source: {source_rows} rows | Target: {target_rows} rows | Diff: {row_difference}",
        )
    )

    null_counts = {}
    for column in CRITICAL_COLUMNS:
        if column in target.columns:
            missing_values = int(target[column].isna().sum())
            if missing_values > 0:
                null_counts[column] = missing_values

    total_nulls = sum(null_counts.values())
    results.append(
        make_result(
            "TC-PD-03",
            "Null Value Check",
            0,
            total_nulls,
            "No nulls found" if total_nulls == 0 else f"Nulls found: {null_counts}",
        )
    )

    duplicate_rows = int(target.duplicated(subset=KEY_COLUMNS, keep=False).sum())
    results.append(
        make_result(
            "TC-PD-04",
            "Duplicate Row Check",
            0,
            duplicate_rows,
            "No duplicates found" if duplicate_rows == 0 else f"{duplicate_rows} duplicate rows found",
        )
    )

    common_row_count = min(len(source), len(target))
    source_measures = source[MEASURE_COLUMNS].iloc[:common_row_count].reset_index(drop=True)
    target_measures = target[MEASURE_COLUMNS].iloc[:common_row_count].reset_index(drop=True)

    diff_dataframe = source_measures.compare(
        target_measures,
        result_names=("Source", "Target"),
    )
    different_rows = len(diff_dataframe)

    results.append(
        make_result(
            "TC-PD-05",
            "Cell-Level Value Diff",
            0,
            different_rows,
            "All values match" if different_rows == 0 else f"{different_rows} rows have different values",
            {"Diff DataFrame": diff_dataframe},
        )
    )

    source_profit = source["Profit"].iloc[:common_row_count].fillna(0).to_numpy()
    target_profit = target["Profit"].iloc[:common_row_count].fillna(0).to_numpy()

    close_matches = np.isclose(source_profit, target_profit, rtol=0.001, atol=0.01)
    profit_mismatches = int((~close_matches).sum())

    results.append(
        make_result(
            "TC-PD-06",
            "Numeric Tolerance Check (Profit)",
            0,
            profit_mismatches,
            (
                "All Profit values are within tolerance"
                if profit_mismatches == 0
                else f"{profit_mismatches} rows exceed tolerance"
            ),
        )
    )

    passed = sum(1 for result in results if result["Status"] == "PASS")
    failed = sum(1 for result in results if result["Status"] == "FAIL")
    print(f"Pandas checks done: {passed} PASSED | {failed} FAILED")

    return results
