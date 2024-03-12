import pytest
from fastapi.testclient import TestClient

from backend.db import Database
from backend.routes import Routes

# Test data for registration
test_register_data = {
    "full_name": "Jose_h",
    "email": "123",
    "password": "thisissecure"
}

# Test data for login
test_login_data = {
    "email": "123",
    "password": "thisissecure"
}

# Plugins required for asyncio testing
pytest_plugins = ('pytest_asyncio',)

# Fixture to setup the database and FastAPI app
@pytest.fixture(scope="module")
def setup():
    async def _setup():
        async with (await Database.connect()) as db:
            routes = Routes(db)
            return routes.get_app()
    return _setup

# Test registration route
@pytest.mark.asyncio
async def test_register(setup):
    app = await setup()
    client = TestClient(app)
    response = client.post("/register", json=test_register_data)
    assert response.status_code == 200
    assert response.json() == {"data": "true"}

# Test login and authentication route
@pytest.mark.asyncio
async def test_login_and_auth(setup):
    app = await setup()
    client = TestClient(app)
    response = client.post("/login", json=test_login_data)
    assert response.status_code == 200
    assert "token" in response.json()
    assert "error" not in response.json()