import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from app.schemas import User, Role
from app.models import Auth0Role

import app.crud.user as users_service


@pytest.fixture
def auth0_mock():
    auth0 = MagicMock()
    auth0.users = MagicMock()
    return auth0


@pytest.fixture
def sample_auth0_user():
    return {
        "user_id": "auth0|123",
        "email": "test@example.com",
        "email_verified": True,
        "nickname": "tester",
        "name": "Test User",
        "created_at": "2024-01-01",
        "updated_at": "2024-01-02",
        "last_login": "2024-01-03",
        "user_metadata": {"associations": ["org1"]},
        "roles": {
            "roles": [
                {"id": "r1", "name": "Admin"},
                {"id": "r2", "name": "User"},
            ]
        },
    }

def test_get_auth0():
    with patch("app.crud.user.GetToken") as token_cls, \
         patch("app.service.user.Auth0") as auth0_cls:

        token_instance = token_cls.return_value
        token_instance.client_credentials.return_value = {
            "access_token": "token"
        }

        users_service.get_auth0()

        token_cls.assert_called_once()
        auth0_cls.assert_called_once_with(
            users_service.config.management_auth0_domain,
            "token"
        )

def test_parse_auth0_user(sample_auth0_user):
    user = users_service.parse_auth0_user(sample_auth0_user)

    assert isinstance(user, User)
    assert user.user_id == "auth0|123"
    assert user.email == "test@example.com"
    assert len(user.roles) == 2
    assert isinstance(user.roles[0], Role)
    assert user.associations == ["org1"]

def test_get_roles_per_user(auth0_mock, sample_auth0_user):
    auth0_mock.users.list_roles.return_value = sample_auth0_user["roles"]

    with patch("app.service.user.get_auth0", return_value=auth0_mock):
        users = users_service.get_roles_per_user([sample_auth0_user])

    assert len(users) == 1
    assert users[0].user_id == "auth0|123"
    auth0_mock.users.list_roles.assert_called_once_with("auth0|123")

@pytest.mark.asyncio
async def test_get_users_with_query(auth0_mock, sample_auth0_user):
    auth0_mock.users.list.return_value = {
        "users": [sample_auth0_user]
    }
    auth0_mock.users.list_roles.return_value = sample_auth0_user["roles"]

    with patch("app.service.user.get_auth0", return_value=auth0_mock):
        users = await users_service.get_users(
            given_name="Test", family_name="User"
        )

    auth0_mock.users.list.assert_called_once()
    assert len(users) == 1

@pytest.mark.asyncio
async def test_get_user_by_id(auth0_mock, sample_auth0_user):
    auth0_mock.users.get.return_value = sample_auth0_user
    auth0_mock.users.list_roles.return_value = sample_auth0_user["roles"]

    with patch("app.service.user.get_auth0", return_value=auth0_mock):
        user = await users_service.get_user_by_id("auth0|123")

    assert user.user_id == "auth0|123"
    auth0_mock.users.get.assert_called_once_with("auth0|123")

@pytest.mark.asyncio
async def test_update_user(auth0_mock, sample_auth0_user):
    auth0_mock.users.update.return_value = {}
    auth0_mock.users.list_roles.return_value = {
        "roles": [{"id": "old-role"}]
    }

    auth0_mock.users.add_roles.return_value = {}
    auth0_mock.users.remove_roles.return_value = {}

    user = users_service.parse_auth0_user(sample_auth0_user)

    with patch("app.service.user.get_auth0", return_value=auth0_mock), \
         patch("app.service.user.get_user_by_id", AsyncMock(return_value=user)):

        result = await users_service.update_user(user)

    auth0_mock.users.update.assert_called_once()
    auth0_mock.users.remove_roles.assert_called_once()
    auth0_mock.users.add_roles.assert_called_once()
    assert result.user_id == "auth0|123"

@pytest.mark.asyncio
async def test_deactivate_user(auth0_mock):
    auth0_mock.users.update.return_value = {}
    auth0_mock.users.list_roles.return_value = {
        "roles": [{"id": "r1"}]
    }

    with patch("app.service.user.get_auth0", return_value=auth0_mock):
        await users_service.deactivate_user("auth0|123")

    auth0_mock.users.update.assert_called_once()
    auth0_mock.users.remove_roles.assert_called_once_with(
        "auth0|123", ["r1"]
    )

@pytest.mark.asyncio
async def test_get_roles():
    session = AsyncMock()
    result = MagicMock()
    role = Auth0Role(id=1, name="Admin")

    result.scalars.return_value.all.return_value = [role]
    session.execute.return_value = result

    roles = await users_service.get_roles(session)

    session.execute.assert_called_once()
    assert roles == [role]
