import pytest

from app.routers import season as seasons_module

from main import app

NOT_AUTHENTICATED = {"detail": "Not authenticated"}

@pytest.mark.asyncio
async def test_read_seasons(test_app):
    expected_results = [
        {"id": "266c4015-6f18-4238-bbcb-7fb70ba1ea90", "name": "Spring 2025",
         "start_dt": "2025-04-05", "season_length": 8, "active": True,
         "holiday_dates": "2025-05-24"}
    ]

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:seasons"}

    app.dependency_overrides[seasons_module.verify_read_seasons] = mock_verify_dependency

    response = await test_app.get("/seasons",
                                 headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_post_seasons_not_authenticated(test_app):
    payload = {
        "name": "Autumn 2025", "start_dt": "2025-01-05",
        "season_length": 8, "active": True
    }

    response = await test_app.post("/seasons",
                                    json=payload)
    assert response.status_code == 403
    assert response.json() == NOT_AUTHENTICATED

@pytest.mark.asyncio
async def test_create_season_success(test_app):
    payload = {
        "name": "Autumn 2025", "start_dt": "2025-01-05",
        "season_length": 8, "active": True
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:seasons"}

    app.dependency_overrides[seasons_module.verify_write_seasons] = mock_verify_dependency

    response = await test_app.post(
        "/seasons",
        json=payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_season_already_exists(test_app):
    payload = {
        "name": "Season Exists", "start_dt": "2025-01-05",
        "season_length": 8, "active": True
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:seasons"}

    # Override the auth verifier used by FastAPI
    app.dependency_overrides[seasons_module.verify_write_seasons] = mock_verify_dependency

    response = await test_app.post(
        "/seasons",
        json=payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201

    response = await test_app.post("/seasons", json=payload,
                                   headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_read_season_by_name_found(test_app):
    expected_results = [{
        "id": "266c4015-6f18-4238-bbcb-7fb70ba1ea90", "name": "Spring 2025",
         "start_dt": "2025-04-05", "season_length": 8, "active": True,
         "holiday_dates": "2025-05-24"
    }]

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:seasons"}

    app.dependency_overrides[seasons_module.verify_read_seasons] = mock_verify_dependency

    response = await test_app.get(
        "/seasons?name=Spring 2025",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_read_season_by_name_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:seasons"}

    app.dependency_overrides[seasons_module.verify_read_seasons] = mock_verify_dependency

    response = await test_app.get(
        "/seasons?name=Spring 2099",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Season, Spring 2099, Not Found"

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_read_season_by_id_found(test_app):
    expected_results = {
        "id": "266c4015-6f18-4238-bbcb-7fb70ba1ea90", "name": "Spring 2025",
         "start_dt": "2025-04-05", "season_length": 8, "active": True,
         "holiday_dates": "2025-05-24"
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:seasons"}

    app.dependency_overrides[seasons_module.verify_read_seasons] = mock_verify_dependency

    response = await test_app.get(
        "/season/266c40156f184238bbcb7fb70ba1ea90",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_read_season_by_id_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:seasons"}

    app.dependency_overrides[seasons_module.verify_read_seasons] = mock_verify_dependency

    response = await test_app.get(
        "/season/266c40156f184248bbcb7fb70ba1ea90",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Season, 266c4015-6f18-4248-bbcb-7fb70ba1ea90, Not Found"

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_delete_season_successfully(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "delete:seasons"}

    app.dependency_overrides[seasons_module.verify_delete_seasons] = mock_verify_dependency

    response = await test_app.delete(
        "/season/266c40156f184238bbcb7fb70ba1ea90",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 204

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_delete_season_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "delete:seasons"}

    app.dependency_overrides[seasons_module.verify_delete_seasons] = mock_verify_dependency

    response = await test_app.delete(
        "/season/266c40156f184248bbcb7fb70ba1ea90",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Failed to Delete, 266c4015-6f18-4248-bbcb-7fb70ba1ea90!"

    app.dependency_overrides.clear()
