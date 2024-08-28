from unittest.mock import AsyncMock
from jose import jwt
import pytest
from app.db.repository.user import UserRepository
from app.service.user import UserService

@pytest.mark.asyncio
async def test_password(user_signup_data):
    user_service = UserService()
    plain_password = user_signup_data.password
    hashed_password = await user_service.hash_password(plain_password)

    assert hashed_password != plain_password
    assert await user_service.verfiy_password(plain_password, hashed_password)
    assert not await user_service.verfiy_password("wrongpassword", hashed_password)

@pytest.mark.asyncio
async def test_create_jwt(user_signup_data):
    user_service = UserService()
    userID = user_signup_data.userID
    token = await user_service.create_jwt(userID)

    assert token is not None
    decoded = jwt.decode(token, user_service.secret_key, algorithms=[user_service.jwt_algorithm])
    assert decoded["sub"] == userID


@pytest.mark.asyncio
async def test_create_user(user_signup_data):
    session = AsyncMock()
    user_repo = UserRepository(session=session)

    session.add.return_value = None
    session.commit.return_value = None
    session.refresh.return_value = None

    user = await user_repo.create_user(user_signup_data)

    assert user.userID == user_signup_data.userID
    assert user.password == user_signup_data.password
    assert session.add.called
    assert session.commit.called
    assert session.refresh.called

@pytest.mark.asyncio
async def test_search_user_by_id(user):
    session = AsyncMock()
    user_repo = UserRepository(session=session)

    session.scalar.return_value = user

    result = await user_repo.search_user_by_id(user.userID)
    assert result == user
    assert session.scalar.called