import pytest
from unittest.mock import patch, AsyncMock

from sqlmodel import Session, SQLModel, create_engine
from app.database import get_session
from app.models import Season
from app.routers import season as seasons_module

from main import app
from fastapi import HTTPException
from fastapi.security import SecurityScopes


NOT_AUTHENTICATED = {"detail": "Not authenticated"}

@pytest.mark.asyncio
async def test_read_seasons(test_app):
    expected_results = [
        {"id": "266c4015-6f18-4238-bbcb-7fb70ba1ea90", "name": "Spring 2025",
         "start_dt": "2025-04-05", "season_length": 8, "active": True,
         "holiday_dates": "2025-05-24"}
    ]

    response = await test_app.get("/seasons")
    assert response.status_code == 200
    assert response.json() == expected_results

@pytest.mark.asyncio
async def test_post_seasons_not_authenticated(test_app):
    season_payload = {
        "name": "Autumn 2025", "start_dt": "2025-01-05",
        "season_length": 8, "active": True
    }

    response = await test_app.post("/seasons",
                                    json=season_payload)
    assert response.status_code == 403
    assert response.json() == NOT_AUTHENTICATED

@pytest.mark.asyncio
async def test_create_season(test_app):
    season_payload = {
        "name": "Autumn 2025", "start_dt": "2025-01-05",
        "season_length": 8, "active": True
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:seasons"}

    # Override the auth verifier used by FastAPI
    app.dependency_overrides[seasons_module.verify_write_seasons] = mock_verify_dependency

    response = await test_app.post(
        "/seasons",
        json=season_payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201
    assert response.json() == season_payload

    seasons_module.create_season.assert_called_once()

    app.dependency_overrides.clear()
