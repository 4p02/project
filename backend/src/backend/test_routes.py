import pytest
from fastapi.testclient import TestClient

from backend.db import Database
from backend.routes import Routes

test_register_data = {
        "full_name":"Jose_h",
        "email": "123",
        "password" : "thisissecure"
    }


test_login_data = {
    "email": "123",
    "password" : "thisissecure"
}

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_register():
    async with (await Database.connect()) as db:
        routes = Routes(db)
        app = routes.get_app()
        client = TestClient(app)
        response = client.post("/register", json=test_register_data)
        assert response.status_code == 200
        assert response.json() == {"data": "true"}
    pass    

