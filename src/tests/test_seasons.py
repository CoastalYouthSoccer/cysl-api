import pytest
from unittest.mock import patch
from sqlmodel import Session, SQLModel, create_engine
from app.database import get_session
from app.models import Season


NOT_AUTHENTICATED = {"detail": "Not authenticated"}

@pytest.mark.anyio
async def test_get_seasons(async_db, async_client):
    print('hi')
    season_1 = Season(name="Test Season", start_dt="2025-01-01",
                      season_length=10, holiday_dates="06/06/2025")
    async_db.add(season_1)
    async_db.commit()

    response = async_client.get("/seasons")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
def test_post_seasons_not_authenticated(test_app):
    response = test_app.post("/seasons")
    assert response.status_code ==403
    assert response.json() == NOT_AUTHENTICATED

#def test_post_seasons(test_app):
#    response = test_app.post("/seasons")
#    assert response.status_code == 201
#    assert response.json() == {"ping": "pong!"}
