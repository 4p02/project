import pytest
from fastapi.testclient import TestClient

from backend.db import Database
from backend.routes import Routes

test_register_data = {
        "fullname":"Jose_h",
        "email": "123@gmail.com",
        "password" : "thisissecure"
    }


test_login_data = {
    "email": "123",
    "password" : "thisissecure"
}

pytest_plugins = ('pytest_asyncio',)


@pytest.fixture
async def test_register():
    async with (await Database.connect()) as db:
        routes = Routes(db)
        app = routes.get_app()
        client = TestClient(app)
        response = client.post("/auth/register", json=test_register_data)
        return response

def test_example(test_register):
    assert test_register.status_code == 200

