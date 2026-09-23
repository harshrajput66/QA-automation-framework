import sqlite3

import pandas as pd


def load_csv(csv_path):
    dataframe = pd.read_csv(csv_path, encoding="latin-1")
    dataframe.columns = dataframe.columns.str.strip().str.lower().str.replace(" ", "_")

    print(f"Loaded CSV: {len(dataframe)} rows")
    return dataframe


def build_dim_customer(dataframe):
    dim_customer = dataframe[["customer_id", "customer_name", "segment"]].drop_duplicates()
    dim_customer.columns = ["CustomerID", "CustomerName", "Segment"]

    print(f"DimCustomer: {len(dim_customer)} rows")
    return dim_customer.reset_index(drop=True)


def build_dim_product(dataframe):
    dim_product = dataframe[["product_id", "category", "sub-category", "product_name"]].drop_duplicates()
    dim_product.columns = ["ProductID", "Category", "SubCategory", "ProductName"]

    print(f"DimProduct: {len(dim_product)} rows")
    return dim_product.reset_index(drop=True)


def build_dim_location(dataframe):
    dim_location = dataframe[["city", "state", "region", "country"]].drop_duplicates()
    dim_location.columns = ["City", "State", "Region", "Country"]
    dim_location.insert(0, "LocationID", range(1, len(dim_location) + 1))

    print(f"DimLocation: {len(dim_location)} rows")
    return dim_location.reset_index(drop=True)


def build_fact_sales(dataframe, dim_location):
    fact_sales = dataframe.merge(
        dim_location,
        left_on=["city", "state", "region", "country"],
        right_on=["City", "State", "Region", "Country"],
        how="left",
    )

    fact_sales = fact_sales[
        [
            "order_id",
            "order_date",
            "ship_date",
            "ship_mode",
            "customer_id",
            "product_id",
            "LocationID",
            "sales",
            "quantity",
            "discount",
            "profit",
        ]
    ]

    fact_sales.columns = [
        "OrderID",
        "OrderDate",
        "ShipDate",
        "ShipMode",
        "CustomerID",
        "ProductID",
        "LocationID",
        "Sales",
        "Quantity",
        "Discount",
        "Profit",
    ]

    print(f"FactSales source: {len(fact_sales)} rows")
    return fact_sales.reset_index(drop=True)


def add_demo_defects(fact_sales):
    if len(fact_sales) < 25:
        raise ValueError("At least 25 rows are needed to add demo defects.")

    target = fact_sales.copy()

    target.loc[0:2, "CustomerID"] = None
    target.loc[3:4, "ProductID"] = "FAKE-PROD-9999"
    target.loc[5, "Sales"] = -999.99
    target.loc[6, "Sales"] = -888.88

    duplicate_rows = target.iloc[10:12].copy()
    target = pd.concat([target, duplicate_rows], ignore_index=True)

    for row_number in range(20, 25):
        target.loc[row_number, "Profit"] = round(target.loc[row_number, "Profit"] + 0.009, 2)

    print(f"FactSales target with demo defects: {len(target)} rows")
    return target


def save_to_sqlite(db_path, dim_customer, dim_product, dim_location, fact_source, fact_target):
    with sqlite3.connect(db_path) as connection:
        dim_customer.to_sql("DimCustomer", connection, if_exists="replace", index=False)
        dim_product.to_sql("DimProduct", connection, if_exists="replace", index=False)
        dim_location.to_sql("DimLocation", connection, if_exists="replace", index=False)
        fact_source.to_sql("FactSales_Source", connection, if_exists="replace", index=False)
        fact_target.to_sql("FactSales_Target", connection, if_exists="replace", index=False)

    print(f"SQLite database saved: {db_path}")


def run_etl(csv_path, db_path):
    raw_data = load_csv(csv_path)

    dim_customer = build_dim_customer(raw_data)
    dim_product = build_dim_product(raw_data)
    dim_location = build_dim_location(raw_data)

    fact_source = build_fact_sales(raw_data, dim_location)
    fact_target = add_demo_defects(fact_source)

    save_to_sqlite(db_path, dim_customer, dim_product, dim_location, fact_source, fact_target)

    return {
        "dim_customer": dim_customer,
        "dim_product": dim_product,
        "dim_location": dim_location,
        "fact_source": fact_source,
        "fact_target": fact_target,
    }
