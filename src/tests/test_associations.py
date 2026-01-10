import pytest
from app.routers import association as associations_module

from main import app

NOT_AUTHENTICATED = {"detail": "Not authenticated"}

@pytest.mark.asyncio(scope="session")
async def test_read_associations(test_app):
    expected_results = [
        {
            "id": "53aeb5c2-590d-4332-8dec-591b1c276d83", "name": "Atlanta",
            "president": None, "secretary": None, "assignor": None, 
            "registrar": None,"active": True
        }, {
            "id": "7297e8d0-0d1c-49c7-a3fa-814b809cfafc", "name": "Chicago",
            "president": None, "secretary": None, "assignor": None, 
            "registrar": None,"active": True
        }, {
            "id": "a3cb9efb-73e8-4758-b547-6b8fb5fd2ba1", "name": "Boston",
            "president": None, "secretary": None, "assignor": None, 
            "registrar": None,"active": True
        }, {
            "id": "d61a1dfb-ebe4-46ac-8210-7e8ecebc7c2d", "name": "Detroit",
            "president": None, "secretary": None, "assignor": None, 
            "registrar": None,"active": True
        }
    ]

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:associations"}

    app.dependency_overrides[associations_module.verify_read_associations] = mock_verify_dependency

    response = await test_app.get("/associations",
                                 headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_post_association_not_authenticated(test_app):
    payload = {
        "name": "Bad Association", "active": True
    }

    response = await test_app.post("/association",
                                    json=payload)
    assert response.status_code == 401
    assert response.json() == NOT_AUTHENTICATED

@pytest.mark.asyncio(scope="session")
async def test_create_association_success(test_app):
    payload = {
        "name": "Good Association", "active": True
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:associations"}

    app.dependency_overrides[associations_module.verify_write_associations] = mock_verify_dependency

    response = await test_app.post(
        "/association",
        json=payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_create_association_already_exists(test_app):
    payload = {
        "name": "Association Exists", "active": True
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:associations"}

    # Override the auth verifier used by FastAPI
    app.dependency_overrides[associations_module.verify_write_associations] = mock_verify_dependency

    response = await test_app.patch(
        "/association",
        json=payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201

    response = await test_app.post("/associations", json=payload,
                                   headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_association_by_name_found(test_app):
    expected_results = [{
        "id": "53aeb5c2-590d-4332-8dec-591b1c276d83", "name": "Atlanta",
        "president": None, "secretary": None, "assignor": None, 
        "registrar": None,"active": True
    }]

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:associations"}

    app.dependency_overrides[associations_module.verify_read_associations] = mock_verify_dependency

    response = await test_app.get(
        "/associations?name=Atlanta",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_association_by_name_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:associations"}

    app.dependency_overrides[associations_module.verify_read_associations] = mock_verify_dependency

    response = await test_app.get(
        "/associations?name=No Association",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Association, No Association, Not Found"

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_association_by_id_found(test_app):
    expected_results = {
        "id": "53aeb5c2-590d-4332-8dec-591b1c276d83", "name": "Atlanta",
        "president": None, "secretary": None, "assignor": None, 
        "registrar": None,"active": True
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:associations"}

    app.dependency_overrides[associations_module.verify_read_associations] = mock_verify_dependency

    response = await test_app.get(
        "/association/53aeb5c2590d43328dec591b1c276d83",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_association_by_id_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:associations"}

    app.dependency_overrides[associations_module.verify_read_associations] = mock_verify_dependency

    response = await test_app.get(
        "/association/266c40156f184248bbcb7fb70ba1ea90",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Association, 266c4015-6f18-4248-bbcb-7fb70ba1ea90, Not Found"

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_delete_association_successfully(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "delete:associations"}

    app.dependency_overrides[associations_module.verify_delete_associations] = mock_verify_dependency

    response = await test_app.delete(
        "/association/53aeb5c2590d43328dec591b1c276d83",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 204

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_delete_association_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "delete:associations"}

    app.dependency_overrides[associations_module.verify_delete_associations] = mock_verify_dependency

    response = await test_app.delete(
        "/association/266c40156f184248bbcb7fb70ba1ea90",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Failed to Delete, 266c4015-6f18-4248-bbcb-7fb70ba1ea90!"

    app.dependency_overrides.clear()
    