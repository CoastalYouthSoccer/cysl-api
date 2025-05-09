import pytest

from app.routers import division as divisions_module

from main import app

NOT_AUTHENTICATED = {"detail": "Not authenticated"}

@pytest.mark.asyncio(scope="session")
async def test_read_divisions(test_app):
    expected_results = [
        {
            "id": "62e3452a-bda7-4e57-83ee-aad9549b400d", "name": "Serie A",
            "active": True
        }, {
            "id": "abc92d02-9717-4c2a-a7e8-e217145abb2c", "name": "D2",
            "active": True
        }, {
            "id": "f6df477c-725c-4452-8883-7116da08a1a4", "name": "D1",
            "active": True
        }
    ]
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:divisions"}

    app.dependency_overrides[divisions_module.verify_read_divisions] = mock_verify_dependency

    response = await test_app.get("/divisions",
                                 headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_post_divisions_not_authenticated(test_app):
    division_payload = {
        "name": "Failed Division", "active": True
    }

    response = await test_app.post("/divisions",
                                    json=division_payload)
    assert response.status_code == 403
    assert response.json() == NOT_AUTHENTICATED

@pytest.mark.asyncio(scope="session")
async def test_create_division_success(test_app):
    division_payload = {
        "name": "Division Works", "active": True
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:divisions"}

    app.dependency_overrides[divisions_module.verify_write_divisions] = mock_verify_dependency

    response = await test_app.post(
        "/divisions",
        json=division_payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_create_division_already_exists(test_app):
    payload = {
        "name": "Division Exists", "active": True
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:divisions"}

    # Override the auth verifier used by FastAPI
    app.dependency_overrides[divisions_module.verify_write_divisions] = mock_verify_dependency

    response = await test_app.post(
        "/divisions",
        json=payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201

    response = await test_app.post("/divisions", json=payload,
                                   headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_division_by_name_found(test_app):
    expected_results = [{
        "id": "f6df477c-725c-4452-8883-7116da08a1a4", "name": "D1",
         "active": True
    }]

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:divisions"}

    app.dependency_overrides[divisions_module.verify_read_divisions] = mock_verify_dependency

    response = await test_app.get(
        "/divisions?name=D1",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_division_by_name_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:divisions"}

    app.dependency_overrides[divisions_module.verify_read_divisions] = mock_verify_dependency

    response = await test_app.get(
        "/divisions?name=D2099",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Division, D2099, Not Found"

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_division_by_id_found(test_app):
    expected_results = {
        "id": "f6df477c-725c-4452-8883-7116da08a1a4", "name": "D1",
        "active": True
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:divisions"}

    app.dependency_overrides[divisions_module.verify_read_divisions] = mock_verify_dependency

    response = await test_app.get(
        "/division/f6df477c725c445288837116da08a1a4",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_division_by_id_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:divisions"}

    app.dependency_overrides[divisions_module.verify_read_divisions] = mock_verify_dependency

    response = await test_app.get(
        "/division/266c40156f184248bbcb7fb70ba1ea90",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Division, 266c4015-6f18-4248-bbcb-7fb70ba1ea90, Not Found"

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_delete_division_successfully(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "delete:divisions"}

    app.dependency_overrides[divisions_module.verify_delete_divisions] = mock_verify_dependency

    response = await test_app.delete(
        "/division/f6df477c725c445288837116da08a1a4",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 204

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_delete_division_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "delete:divisions"}

    app.dependency_overrides[divisions_module.verify_delete_divisions] = mock_verify_dependency

    response = await test_app.delete(
        "/division/266c40156f184248bbcb7fb70ba1ea90",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Failed to Delete, 266c4015-6f18-4248-bbcb-7fb70ba1ea90!"

    app.dependency_overrides.clear()
