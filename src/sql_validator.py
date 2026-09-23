import sqlite3

import pandas as pd


def get_single_value(connection, query):
    return pd.read_sql_query(query, connection).iloc[0, 0]


def make_result(test_id, test_name, expected, actual, details):
    return {
        "Test ID": test_id,
        "Test Name": test_name,
        "Expected": expected,
        "Result": actual,
        "Status": "PASS" if expected == actual else "FAIL",
        "Details": details,
    }


def run_sql_checks(db_path):
    print("Running SQL checks...")

    results = []

    with sqlite3.connect(db_path) as connection:
        null_count = get_single_value(
            connection,
            """
            SELECT COUNT(*)
            FROM FactSales_Target
            WHERE CustomerID IS NULL
               OR ProductID IS NULL
               OR LocationID IS NULL
            """,
        )
        results.append(
            make_result(
                "TC-SQL-01",
                "Null Check on Key Columns",
                0,
                null_count,
                f"{null_count} rows have missing key values",
            )
        )

        duplicate_groups = get_single_value(
            connection,
            """
            SELECT COUNT(*)
            FROM (
                SELECT OrderID, CustomerID, ProductID, COUNT(*) AS row_count
                FROM FactSales_Target
                GROUP BY OrderID, CustomerID, ProductID
                HAVING COUNT(*) > 1
            )
            """,
        )
        results.append(
            make_result(
                "TC-SQL-02",
                "Duplicate Row Check",
                0,
                duplicate_groups,
                f"{duplicate_groups} duplicate OrderID + CustomerID + ProductID groups found",
            )
        )

        orphan_customers = get_single_value(
            connection,
            """
            SELECT COUNT(*)
            FROM FactSales_Target f
            LEFT JOIN DimCustomer d ON f.CustomerID = d.CustomerID
            WHERE d.CustomerID IS NULL
              AND f.CustomerID IS NOT NULL
            """,
        )
        results.append(
            make_result(
                "TC-SQL-03",
                "Orphan CustomerID Check",
                0,
                orphan_customers,
                f"{orphan_customers} CustomerIDs were not found in DimCustomer",
            )
        )

        orphan_products = get_single_value(
            connection,
            """
            SELECT COUNT(*)
            FROM FactSales_Target f
            LEFT JOIN DimProduct d ON f.ProductID = d.ProductID
            WHERE d.ProductID IS NULL
              AND f.ProductID IS NOT NULL
            """,
        )
        results.append(
            make_result(
                "TC-SQL-04",
                "Orphan ProductID Check",
                0,
                orphan_products,
                f"{orphan_products} ProductIDs were not found in DimProduct",
            )
        )

        negative_sales = get_single_value(
            connection,
            """
            SELECT COUNT(*)
            FROM FactSales_Target
            WHERE Sales < 0
            """,
        )
        results.append(
            make_result(
                "TC-SQL-05",
                "Negative Sales Check",
                0,
                negative_sales,
                f"{negative_sales} rows have negative Sales values",
            )
        )

        source_rows = get_single_value(connection, "SELECT COUNT(*) FROM FactSales_Source")
        target_rows = get_single_value(connection, "SELECT COUNT(*) FROM FactSales_Target")
        results.append(
            make_result(
                "TC-SQL-06",
                "Row Count Check",
                source_rows,
                target_rows,
                f"Source: {source_rows} rows | Target: {target_rows} rows",
            )
        )

        source_sales = round(get_single_value(connection, "SELECT SUM(Sales) FROM FactSales_Source"), 2)
        target_sales = round(get_single_value(connection, "SELECT SUM(Sales) FROM FactSales_Target"), 2)
        sales_difference = round(abs(source_sales - target_sales), 2)

        results.append(
            {
                "Test ID": "TC-SQL-07",
                "Test Name": "Total Sales Rollup Check",
                "Expected": source_sales,
                "Result": target_sales,
                "Status": "PASS" if sales_difference < 1.0 else "FAIL",
                "Details": (
                    f"Source Total: ${source_sales} | "
                    f"Target Total: ${target_sales} | "
                    f"Diff: ${sales_difference}"
                ),
            }
        )

    passed = sum(1 for result in results if result["Status"] == "PASS")
    failed = sum(1 for result in results if result["Status"] == "FAIL")
    print(f"SQL checks done: {passed} PASSED | {failed} FAILED")

    return results
