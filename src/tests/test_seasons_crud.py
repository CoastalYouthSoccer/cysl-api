import pytest
import uuid
from fastapi import HTTPException

from app.models.season import Season, SeasonCreate
from app.crud.season import (create_season, get_season_by_id, get_seasons,
                             get_season_by_name)
from datetime import date

@pytest.mark.asyncio
async def test_create_season(db_session):
    season_data = SeasonCreate(
        name="Fall 2025",
        start_dt=date(2025, 9, 1),
        season_length=10,
        holiday_dates="2025-10-10,2025-11-25"
    )
    season = await create_season(db_session, season_data)

    assert season.id is not None
    assert season.name == "Fall 2025"
    assert season.season_length == 10
    assert season.holiday_dates == "2025-10-10,2025-11-25"

@pytest.mark.asyncio
async def test_create_season_already_exists(db_session):
    season_data = SeasonCreate(
        name="Spring 2025",
        start_dt=date(2025,4,5),
        season_length=8,
        holiday_dates="2025-05-24"
    )

    with pytest.raises(HTTPException) as exc_info:
        await create_season(db_session, season_data)

    exception = exc_info.value
    assert exception.status_code == 409
    assert "Season, Spring 2025, already exists!" in exception.detail

@pytest.mark.asyncio
async def test_get_season_by_id(db_session):
    season_data = SeasonCreate(
        name="Spring 2026",
        start_dt=date(2026, 3, 1),
        season_length=8
    )
    created = await create_season(db_session, season_data)
    found = await get_season_by_id(db_session, created.id)

    assert found is not None
    assert found.name == "Spring 2026"
    assert found.start_dt == date(2026, 3, 1)

@pytest.mark.asyncio
async def test_get_season_by_id_not_found(db_session):
    with pytest.raises(HTTPException) as exc_info:
        await get_season_by_id(db_session,
                                uuid.UUID("3c34837a-390d-4af9-a408-cc4587fe8b86"))
    exception = exc_info.value
    assert exception.status_code == 404
    assert "Season, 3c34837a-390d-4af9-a408-cc4587fe8b86, Not Found" in exception.detail
