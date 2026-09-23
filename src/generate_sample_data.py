import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

CUSTOMERS = [
    ("CG-12520", "Claire Gute",       "Consumer"),
    ("DV-13045", "Darrin Van Huff",   "Corporate"),
    ("SO-20335", "Sean O'Donnell",    "Consumer"),
    ("BH-11710", "Brosina Hoffman",   "Consumer"),
    ("AA-10480", "Andrew Allen",      "Consumer"),
    ("IM-15070", "Irene Maddox",      "Consumer"),
    ("HP-14815", "Harold Pawlan",     "Home Office"),
    ("PK-19075", "Pete Kriz",         "Consumer"),
    ("AG-10270", "Alejandro Grove",   "Consumer"),
    ("ZD-21925", "Zuschuss Donatelli","Consumer"),
    ("KB-16585", "Karl Braun",        "Consumer"),
    ("MA-17560", "Mick Hernandez",    "Corporate"),
    ("LC-17050", "Laura Coffey",      "Consumer"),
    ("NK-18640", "Nicole Klein",      "Consumer"),
    ("DO-13210", "Dario Oten",        "Home Office"),
]

PRODUCTS = [
    ("FUR-BO-10001798", "Furniture",  "Bookcases",  "Bush Somerset Collection Bookcase"),
    ("FUR-CH-10000454", "Furniture",  "Chairs",     "Hon Deluxe Fabric Upholstered Stacking Chairs"),
    ("OFF-LA-10000240", "Office Supplies", "Labels","Self-Adhesive Address Labels"),
    ("FUR-TA-10000577", "Furniture",  "Tables",     "Bretford CR4500 Series Slim Rectangular Table"),
    ("OFF-ST-10000760", "Office Supplies", "Storage","Eldon Fold 'N Roll Cart System"),
    ("FUR-FU-10001487", "Furniture",  "Furnishings","Eldon Expressions Wood and Plastic Desk Accessories"),
    ("OFF-AR-10002833", "Office Supplies", "Art",   "Newell 322"),
    ("TEC-PH-10002033", "Technology", "Phones",     "Mitel 5320 IP Phone VoIP phone"),
    ("OFF-BI-10003910", "Office Supplies", "Binders","DXL Angle-View Binders with Locking Rings"),
    ("OFF-AP-10002311", "Office Supplies", "Appliances","Belkin F5C206VTEL06 "),
    ("OFF-PA-10001970", "Office Supplies", "Paper",  "HP Copy Paper"),
    ("TEC-PH-10001949", "Technology", "Phones",     "Samsung Galaxy"),
    ("TEC-CO-10004722", "Technology", "Copiers",    "Canon PC940 Copier"),
    ("TEC-AC-10003832", "Technology", "Accessories","Plantronics CS510"),
    ("OFF-EN-10001500", "Office Supplies", "Envelopes","Poly String Tie Envelopes"),
]

LOCATIONS = [
    ("Henderson",    "Kentucky",       "South",   "United States"),
    ("Los Angeles",  "California",     "West",    "United States"),
    ("Fort Lauderdale","Florida",      "South",   "United States"),
    ("Concord",      "North Carolina", "South",   "United States"),
    ("Seattle",      "Washington",     "West",    "United States"),
    ("Fort Worth",   "Texas",          "Central", "United States"),
    ("Madison",      "Wisconsin",      "Central", "United States"),
    ("West Jordan",  "Utah",           "West",    "United States"),
    ("San Francisco","California",     "West",    "United States"),
    ("Philadelphia", "Pennsylvania",   "East",    "United States"),
    ("New York City","New York",       "East",    "United States"),
    ("Houston",      "Texas",          "Central", "United States"),
    ("Columbus",     "Ohio",           "East",    "United States"),
    ("Springfield",  "Illinois",       "Central", "United States"),
    ("Denver",       "Colorado",       "West",    "United States"),
]

SHIP_MODES = ["Second Class", "Standard Class", "First Class", "Same Day"]


def random_date(start_year=2020, end_year=2024):
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def generate_superstore_data(n_rows: int = 1000) -> pd.DataFrame:
    rows = []

    for i in range(1, n_rows + 1):
        cust     = random.choice(CUSTOMERS)
        prod     = random.choice(PRODUCTS)
        loc      = random.choice(LOCATIONS)
        ship     = random.choice(SHIP_MODES)
        order_dt = random_date()
        ship_dt  = order_dt + timedelta(days=random.randint(1, 7))

        sales    = round(random.uniform(10.0, 2500.0), 2)
        qty      = random.randint(1, 10)
        discount = round(random.choice([0.0, 0.1, 0.2, 0.3, 0.4, 0.5]), 2)
        profit   = round(sales * random.uniform(-0.15, 0.40), 2)

        rows.append({
            "Row ID":       i,
            "Order ID":     f"CA-{order_dt.year}-{random.randint(100000, 199999)}",
            "Order Date":   order_dt.strftime("%d/%m/%Y"),
            "Ship Date":    ship_dt.strftime("%d/%m/%Y"),
            "Ship Mode":    ship,
            "Customer ID":  cust[0],
            "Customer Name":cust[1],
            "Segment":      cust[2],
            "Country":      loc[3],
            "City":         loc[0],
            "State":        loc[1],
            "Postal Code":  str(random.randint(10000, 99999)),
            "Region":       loc[2],
            "Product ID":   prod[0],
            "Category":     prod[1],
            "Sub-Category": prod[2],
            "Product Name": prod[3],
            "Sales":        sales,
            "Quantity":     qty,
            "Discount":     discount,
            "Profit":       profit,
        })

    df = pd.DataFrame(rows)
    print(f"[INFO] Generated {len(df)} rows of Superstore sample data.")
    return df


def create_sample_csv(output_path: str = os.path.join("data", "kaggle_sales_raw.csv"),
                      n_rows: int = 1000):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = generate_superstore_data(n_rows)
    df.to_csv(output_path, index=False, encoding="latin-1")
    print(f"[INFO] Sample dataset saved to: {output_path}")
    print("[INFO] To use the real Kaggle data, replace this file with:")
    print("       https://www.kaggle.com/datasets/vivek468/superstore-dataset-final\n")
    return df


if __name__ == "__main__":
    create_sample_csv()
