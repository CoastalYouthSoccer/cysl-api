import pytest
from unittest.mock import patch, MagicMock
from app.crud.user import (get_users, get_user_by_id, 
                           deactivate_user, update_user)

from app.schemas import User

# Mock return values for CRUD operations
@pytest.fixture(autouse=True)
def mock_crud(monkeypatch):
    monkeypatch.setattr("app.crud.get_users", lambda *args, **kwargs: [User(
        user_id="google-oauth2|123",
        email="test@example.com",
        email_verified=True,
        user_name="testuser",
        created_dt="2025-01-01T00:00:00",
        updated_dt="2025-01-02T00:00:00",
        user_metadata={"association": ["Hanover"]},
        name="Test User",
        last_login="2025-01-03T00:00:00",
        given_name="Test",
        family_name="User",
        roles=[],
        associations=["Hanover"]
    )])

    monkeypatch.setattr("app.crud.get_user_by_id", lambda id: User(
        user_id=id,
        email="test@example.com",
        email_verified=True,
        user_name="testuser",
        created_dt="2025-01-01T00:00:00",
        updated_dt="2025-01-02T00:00:00",
        user_metadata={"association": ["Hanover"]},
        name="Test User",
        last_login="2025-01-03T00:00:00",
        given_name="Test",
        family_name="User",
        roles=[],
        associations=["Hanover"]
    ))

    monkeypatch.setattr("app.crud.update_user", lambda user: user)
    monkeypatch.setattr("app.crud.deactivate_user", lambda id: None)

@pytest.mark.asyncio
@patch("app.crud.user.get_auth0")
async def test_read_users(mock_get_auth0):
    mock_auth0 = MagicMock()
    mock_auth0.users.list_roles.return_value = [
        {"id": "rol_123", "name": "admin", "description": "Administrator"}
    ]
    mock_get_auth0.return_value = mock_auth0

    result = await get_users()

@pytest.mark.asyncio
@patch("app.crud.user.get_auth0")
async def test_get_user_id(mock_get_auth0):
    mock_auth0 = MagicMock()
    mock_auth0.users.list_roles.return_value = [
        {"id": "rol_123", "name": "admin", "description": "Administrator"}
    ]
    mock_get_auth0.return_value = mock_auth0
    result = await get_user_by_id("/user/google-oauth2|123")


@pytest.mark.asyncio
@patch("app.crud.user.get_auth0")
async def test_change_user(mock_get_auth0):
    mock_auth0 = MagicMock()
    mock_auth0.users.list_roles.return_value = [
        {"id": "rol_123", "name": "admin", "description": "Administrator"}
    ]
    mock_get_auth0.return_value = mock_auth0
    result = await update_user("/user", json={
        "user_id": "google-oauth2|123",
        "email": "test@example.com",
        "email_verified": True,
        "user_name": "testuser",
        "created_dt": "2025-01-01T00:00:00",
        "updated_dt": "2025-01-02T00:00:00",
        "user_metadata": {"association": ["Hanover"]},
        "name": "Test User",
        "last_login": "2025-01-03T00:00:00",
        "given_name": "Test",
        "family_name": "User",
        "roles": [],
        "associations": ["Hanover"]
    })

@pytest.mark.asyncio
@patch("app.crud.user.get_auth0")
async def test_delete_user(mock_get_auth0):
    mock_auth0 = MagicMock()
    mock_auth0.users.list_roles.return_value = [
        {"id": "rol_123", "name": "admin", "description": "Administrator"}
    ]
    mock_get_auth0.return_value = mock_auth0
    result = await deactivate_user("/user/google-oauth2|123")
