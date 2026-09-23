from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
VALID_CSV_PATH = DATA_DIR / "kaggle_sales_raw.csv"


def create_valid_test_csv(tmp_path):
    csv_content = (
        "Row ID,Order ID,Order Date,Ship Date,Ship Mode,Customer ID,"
        "Customer Name,Segment,Country,City,State,Postal Code,Region,"
        "Product ID,Category,Sub-Category,Product Name,Sales,Quantity,Discount,Profit\n"
        "1,CA-2020-100001,01/01/2020,05/01/2020,Standard Class,CG-12520,"
        "Claire Gute,Consumer,United States,Henderson,Kentucky,42420,South,"
        "FUR-BO-10001798,Furniture,Bookcases,Bush Somerset Collection Bookcase,"
        "261.96,2,0.0,41.91\n"
        "2,CA-2020-100002,02/01/2020,06/01/2020,Second Class,DV-13045,"
        "Darrin Van Huff,Corporate,United States,Los Angeles,California,90036,West,"
        "OFF-LA-10000240,Office Supplies,Labels,Self-Adhesive Address Labels,"
        "14.62,2,0.0,6.87\n"
    )
    csv_path = tmp_path / "test_upload.csv"
    csv_path.write_text(csv_content, encoding="utf-8")
    return csv_path


def create_invalid_csv(tmp_path):
    csv_path = tmp_path / "invalid.csv"
    csv_path.write_text("not,a,valid,csv\nwith,wrong,columns,here\n", encoding="utf-8")
    return csv_path


def create_empty_file(tmp_path):
    empty_path = tmp_path / "empty.csv"
    empty_path.write_text("", encoding="utf-8")
    return empty_path


def create_non_csv_file(tmp_path):
    txt_path = tmp_path / "document.txt"
    txt_path.write_text("This is not a CSV file.", encoding="utf-8")
    return txt_path
