import pytest

@pytest.mark.asyncio
async def test_user_sign_up(client, user_signup_data):

    response = await client.post("/user/sign-up", json=user_signup_data.dict())

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_user_sign_in(client, user):

    response = await client.post(
        "/user/sign-in",
        json={"userID": user.userID, "password": user.password},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


