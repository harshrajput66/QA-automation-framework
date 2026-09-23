"""
Root conftest.py — shared fixtures for the entire test suite.

Provides:
  - Flask app instance
  - Flask test server (starts in a background thread for UI/API tests)
  - Temporary directory for test files
"""
import sys
import threading
import time
from pathlib import Path

import pytest

# Ensure project root and src/ are on the path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))


@pytest.fixture(scope="session")
def app():
    """Create and configure the Flask application for testing."""
    from app import app as flask_app
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test-secret-key"
    return flask_app


@pytest.fixture(scope="session")
def flask_server(app):
    """
    Start the Flask dev server in a background thread for the test session.
    This is used by both API tests (requests) and UI tests (Playwright).
    """
    from tests.utils.config import APP_HOST, APP_PORT

    server_thread = threading.Thread(
        target=lambda: app.run(host=APP_HOST, port=APP_PORT, use_reloader=False),
        daemon=True,
    )
    server_thread.start()

    # Wait for the server to be ready
    import requests
    base_url = f"http://{APP_HOST}:{APP_PORT}"
    for _ in range(30):
        try:
            resp = requests.get(base_url, timeout=1)
            if resp.status_code in (200, 302):
                break
        except requests.ConnectionError:
            time.sleep(0.5)
    else:
        pytest.fail("Flask server did not start in time")

    yield base_url


@pytest.fixture(scope="session")
def base_url(flask_server):
    """Provide the base URL of the running Flask server."""
    return flask_server


@pytest.fixture
def test_files(tmp_path):
    """Provide a temporary directory for test file creation."""
    return tmp_path
