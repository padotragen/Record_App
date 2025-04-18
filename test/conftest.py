# tests/conftest.py

import pytest
from recordapp import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for tests
    with flask_app.test_client() as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def warmup_cache():
    """
    Automatically warm up the Discogs API cache at the start of the test session.
    This avoids slow first-time loads in individual tests.
    """
    with flask_app.test_client() as client:
        client.get("/collection?filter=Kings+of+Leon")
        client.get("/carousel?filter=Kings+of+Leon")
        client.get("/collection")
        client.get("/release?id=1471516")
