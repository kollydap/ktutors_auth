import pytest
from fastapi.testclient import TestClient
from app.core.application import get_app


@pytest.fixture(autouse=False)
async def route_test_client():
    app = get_app()

    with TestClient(app=app, raise_server_exceptions=False) as test_client:
        yield test_client