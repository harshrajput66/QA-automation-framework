"""
Conftest for data/database tests.

Provides fixtures that run the ETL pipeline once per session and
expose the database path and DataFrames to individual test functions.
"""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from tests.utils.config import CSV_PATH, DB_PATH


@pytest.fixture(scope="session")
def etl_output():
    """
    Run the ETL pipeline once for the entire data test session.
    Returns the tables dict from kaggle_loader.run_etl().
    """
    from kaggle_loader import run_etl
    from generate_sample_data import create_sample_csv

    # Ensure CSV exists
    if not CSV_PATH.exists():
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        create_sample_csv(output_path=str(CSV_PATH), n_rows=1000)

    tables = run_etl(str(CSV_PATH), str(DB_PATH))
    return tables


@pytest.fixture(scope="session")
def db_path(etl_output):
    """Path to the populated SQLite database."""
    return str(DB_PATH)


@pytest.fixture(scope="session")
def source_df(etl_output):
    """Source FactSales DataFrame (before defects)."""
    return etl_output["fact_source"]


@pytest.fixture(scope="session")
def target_df(etl_output):
    """Target FactSales DataFrame (with injected defects)."""
    return etl_output["fact_target"]
