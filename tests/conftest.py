"""
tests.conftest.py
~~~~~~~~~~~~~~~~~
"""

import pytest
from fastapi.testclient import TestClient

from api import main


@pytest.fixture(scope="session")
def api_client():
    """FastAPI testing client"""
    return TestClient(main.app)
