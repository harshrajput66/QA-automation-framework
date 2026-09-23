import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from tests.utils.config import CSV_PATH, DB_PATH


@pytest.fixture(scope="session")
def etl_output():
    from kaggle_loader import run_etl
    from generate_sample_data import create_sample_csv

    if not CSV_PATH.exists():
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        create_sample_csv(output_path=str(CSV_PATH), n_rows=1000)

    tables = run_etl(str(CSV_PATH), str(DB_PATH))
    return tables


@pytest.fixture(scope="session")
def db_path(etl_output):
    return str(DB_PATH)


@pytest.fixture(scope="session")
def source_df(etl_output):
    return etl_output["fact_source"]


@pytest.fixture(scope="session")
def target_df(etl_output):
    return etl_output["fact_target"]
