import pytest
from app.schemas import user as user_schema
from app.main import app
from httpx import AsyncClient
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def client():
    return AsyncClient(app=app, base_url="http://localhost:8000")

@pytest.fixture
def user_signup_data():
    return user_schema.UserSignup(
        userID="testuser",
        password="testpassword",
        email="test@example.com",
        userName="Test User",
        phone="1234567890",
        birthday="2000-01-01",
        address="123 Test St",
    )

@pytest.fixture
def user():
    return user_schema.UserLogin(
        userID="testuser",
        password="testpassword"
    )
    

