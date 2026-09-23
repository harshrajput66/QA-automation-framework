"""
Conftest for API tests.

Provides the API client fixture and ensures the Flask server is running.
"""
import pytest

from tests.utils.config import BASE_URL


@pytest.fixture
def api_client(flask_server):
    """Provide a configured APIClient pointing at the running Flask server."""
    from tests.api.api_client import APIClient
    return APIClient(base_url=flask_server)
