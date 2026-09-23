import sys
import threading
import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))


@pytest.fixture(scope="session")
def app():
    from app import app as flask_app
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test-secret-key"
    return flask_app


@pytest.fixture(scope="session")
def flask_server(app):
    from tests.utils.config import APP_HOST, APP_PORT

    server_thread = threading.Thread(
        target=lambda: app.run(host=APP_HOST, port=APP_PORT, use_reloader=False),
        daemon=True,
    )
    server_thread.start()

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
    return flask_server


@pytest.fixture
def test_files(tmp_path):
    return tmp_path
