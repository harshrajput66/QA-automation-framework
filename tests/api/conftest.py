import pytest

from tests.utils.config import BASE_URL


@pytest.fixture
def api_client(flask_server):
    from tests.api.api_client import APIClient
    return APIClient(base_url=flask_server)
