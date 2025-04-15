import pytest
from unittest.mock import patch, AsyncMock

from sqlmodel import Session, SQLModel, create_engine
from app.database import get_session
from app.models import Season
from main import app
from fastapi import HTTPException
from fastapi.security import SecurityScopes


NOT_AUTHENTICATED = {"detail": "Not authenticated"}

@pytest.fixture(autouse=True)
def override_get_session(mock_session):
    app.dependency_overrides[get_session] = lambda: mock_session
    yield
    app.dependency_overrides.clear()

# Mock auth.verify (security dependency)
@pytest.fixture(autouse=True)
def override_auth_verify():
    def fake_verify(security_scopes: SecurityScopes, token: str = ""):
        required_scopes = set(security_scopes.scopes)
        granted_scopes = {"read:seasons", "write:seasons",
                          "delete:seasons"} 

        if not required_scopes.issubset(granted_scopes):
            raise HTTPException(status_code=403, detail="Insufficient scope")

        return "mock-user-id"
    from app.dependencies import auth as auth_module
    auth_module.verify = fake_verify
    yield

@pytest.mark.asyncio
async def test_read_seasons(test_app, mock_session):
    fake_data = [
        {"id": "fd305323-51bb-405f-8e01-2cf30d49794a", "name": "Summer",
         "start_dt": "2025-04-05", "season_length": 8, "active": True,
         "holiday_dates": None},
        {"id": "d2324a88-2a89-4da5-9c22-769ea9cb27ee", "name": "Fall",
         "start_dt": "2025-09-05", "season_length": 8, "active": True,
         "holiday_dates": None},
    ]

    # Patch the service layer function directly
    import app.routers.season as seasons_module
    seasons_module.get_seasons = AsyncMock(return_value=fake_data)

    response = await test_app.get("/seasons")
    assert response.status_code == 200
    assert response.json() == fake_data

@pytest.mark.asyncio
def test_post_seasons_not_authenticated(test_app):
    response = test_app.post("/seasons")
    assert response.status_code ==403
    assert response.json() == NOT_AUTHENTICATED

@pytest.mark.asyncio
async def test_create_season(test_app):
    season_payload = {
        "name": "Autumn 2025", "start_dt": "2025-01-05",
        "season_length": 8, "active": True,
        "holiday_dates": None
    }

    import app.routers.season as seasons_module
    seasons_module.create_season = AsyncMock(return_value=season_payload)

    response = await test_app.post(
        "/seasons",
        json=season_payload,
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 201
    assert response.json() == season_payload
    seasons_module.create_season.assert_called_once()
