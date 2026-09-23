import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

BASE_URL = os.environ.get("QA_BASE_URL", "http://localhost:5000")
APP_HOST = "127.0.0.1"
APP_PORT = 5000

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"
INVALID_USERNAME = "wrong_user"
INVALID_PASSWORD = "wrong_pass"

DATA_DIR = PROJECT_ROOT / "data"
CSV_PATH = DATA_DIR / "kaggle_sales_raw.csv"
DB_PATH = DATA_DIR / "target_dwh.db"
REPORT_PATH = PROJECT_ROOT / "QA_Test_Execution_Report.xlsx"
TEST_CASE_PATH = PROJECT_ROOT / "TestCases.xlsx"

DEFAULT_TIMEOUT = 30000
API_TIMEOUT = 10

HEADLESS = os.environ.get("QA_HEADLESS", "true").lower() == "true"
SLOW_MO = int(os.environ.get("QA_SLOW_MO", "0"))
BROWSER = os.environ.get("QA_BROWSER", "chromium")

SCREENSHOT_ON_FAILURE = True
TRACE_ON_FAILURE = True
VIDEO_RECORDING = os.environ.get("QA_VIDEO", "false").lower() == "true"
