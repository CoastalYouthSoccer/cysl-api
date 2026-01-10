import pytest
from app.routers import venue as venues_module

from main import app

NOT_AUTHENTICATED = {"detail": "Not authenticated"}

@pytest.mark.asyncio(scope="session")
async def test_read_venues(test_app):

    expected_results = [
        {
            'active': True, 'name': 'Boston Venue 1', 'address':
            {
                'active': True, 'address1': '85 Main St',
                'address2': None, 'city': 'Boston',
                'state': 'MA', 'zip_code': '02135'
            },
            'association_id': 'a3cb9efb-73e8-4758-b547-6b8fb5fd2ba1',
            'id': 'a6d69d3e-de15-4d4e-8c18-5aa6252f0bd3'
        }, {
            'active': True, 'name': 'Atlanta Venue', 'address':
            {
                'active': True, 'address1': '100 Main Street',
                'address2': None, 'city': 'Atlanta',
                'state': 'GA', 'zip_code': '30303'
            },
            'association_id': '53aeb5c2-590d-4332-8dec-591b1c276d83',
            'id': 'b6a95d67-9542-49a5-9e20-b4732fd68309' 
        }, {           
            'active': True, 'name': 'Boston Venue 2', 'address':
            {
                'active': True, 'address1': '20 Maple St.',
                'address2': None, 'city': 'Boston',
                'state': 'MA', 'zip_code': '02132'
            },
            'association_id': 'a3cb9efb-73e8-4758-b547-6b8fb5fd2ba1',
            'id': 'ec9e8bf0-2c86-4bc9-b1eb-f52166c930ff'
        }
    ]

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:venues"}

    app.dependency_overrides[venues_module.verify_read_venues] = mock_verify_dependency

    response = await test_app.get("/venues",
                                 headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_post_venues_not_authenticated(test_app):
    payload = {
        "name": "Bad Association", "active": True
    }

    response = await test_app.post("/venue",
                                    json=payload)
    assert response.status_code == 401
    assert response.json() == NOT_AUTHENTICATED

@pytest.mark.asyncio(scope="session")
async def test_create_venue_new_address(test_app):
    payload = {
        "name": "New Address",
        "active": True,
        "address": {
            "address1": "123 Home Run Ave",
            "address2": "Suite B",
            "city": "Baseball Town",
            "state": "CA",
            "zip_code": "90210"

        },
        "association_id": "53aeb5c2-590d-4332-8dec-591b1c276d83"
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:venues"}

    app.dependency_overrides[venues_module.verify_write_venues] = mock_verify_dependency

    response = await test_app.post(
        "/venue",
        json=payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_update_venue_existing_address(test_app):
    payload = {
        "name": "Existing Address",
        "active": True,
        "address": {
            "address1": "100 Main Street",
            "city": "Atlanta",
            "state": "GA",
            "zip_code": "30303"
        },
        "association_id": "53aeb5c2-590d-4332-8dec-591b1c276d83"
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:venues"}

    app.dependency_overrides[venues_module.verify_write_venues] = mock_verify_dependency

    response = await test_app.patch(
        "/venue",
        json=payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_create_venue_already_exists(test_app):
    payload = {
        "name": "Venue Exists",
        "active": True,
        "address": {
            "address1": "200 Main Street",
            "city": "Atlanta",
            "state": "GA",
            "zip_code": "30303"
        },
        "association_id": "53aeb5c2-590d-4332-8dec-591b1c276d83"
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:venues"}

    # Override the auth verifier used by FastAPI
    app.dependency_overrides[venues_module.verify_write_venues] = mock_verify_dependency

    response = await test_app.post(
        "/venue",
        json=payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201

    response = await test_app.post("/venue", json=payload,
                                   headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_create_venue_invalid_association(test_app):
    payload = {
        "name": "No Association",
        "active": True,
        "address": {
            "address1": "100 Main Street",
            "city": "Atlanta",
            "state": "GA",
            "zip_code": "30303"
        },
        "association_id": "53aeb5c2-590d-4332-8dec-591b1c276d84"
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "write:venues"}

    app.dependency_overrides[venues_module.verify_write_venues] = mock_verify_dependency

    response = await test_app.post(
        "/venue",
        json=payload,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Association, 53aeb5c2-590d-4332-8dec-591b1c276d84, Not Found"

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_venue_by_name_found(test_app):
    expected_results = [
        {
            'active': True, 'name': 'Atlanta Venue', 'address':
            {
                'active': True, 'address1': '100 Main Street',
                'address2': None, 'city': 'Atlanta',
                'id': '41a6ae75-aa9d-4c19-857d-0be3c95f703a',
                'state': 'GA', 'zip_code': '30303'
            },
            'association_id': '53aeb5c2-590d-4332-8dec-591b1c276d83',
            'id': 'b6a95d67-9542-49a5-9e20-b4732fd68309' 
        }
    ]

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:venues"}

    app.dependency_overrides[venues_module.verify_read_venues] = mock_verify_dependency

    response = await test_app.get(
        "/venues?name=Atlanta Venue",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_venue_by_name_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:venues"}

    app.dependency_overrides[venues_module.verify_read_venues] = mock_verify_dependency

    response = await test_app.get(
        "/venues?name=No Venue",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Venue, No Venue, Not Found"

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_venue_by_id_found(test_app):
    expected_results = {
        'active': True, 'name': 'Boston Venue 1', 'address':
        {
            'active': True, 'address1': '85 Main St',
            'address2': None, 'city': 'Boston',
            'state': 'MA', 'zip_code': '02135',
            'id': '558a0e81-ea45-4e3b-ac9d-936a75136ef5'
        },
        'association_id': 'a3cb9efb-73e8-4758-b547-6b8fb5fd2ba1',
        'id': 'a6d69d3e-de15-4d4e-8c18-5aa6252f0bd3'
    }

    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:venues"}

    app.dependency_overrides[venues_module.verify_read_venues] = mock_verify_dependency

    response = await test_app.get(
        "/venue/a6d69d3ede154d4e8c185aa6252f0bd3",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    assert response.json() == expected_results

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_read_venue_by_id_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "read:venues"}

    app.dependency_overrides[venues_module.verify_read_venues] = mock_verify_dependency

    response = await test_app.get(
        "/venue/266c40156f184248bbcb7fb70ba1ea90",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Venue, 266c4015-6f18-4248-bbcb-7fb70ba1ea90, Not Found"

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_delete_venue_successfully(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "delete:venues"}

    app.dependency_overrides[venues_module.verify_delete_venues] = mock_verify_dependency

    response = await test_app.delete(
        "/venue/ec9e8bf02c864bc9b1ebf52166c930ff",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 204

    app.dependency_overrides.clear()

@pytest.mark.asyncio(scope="session")
async def test_delete_venue_not_found(test_app):
    async def mock_verify_dependency():
        return {"sub": "test_user",
                "scope": "delete:venues"}

    app.dependency_overrides[venues_module.verify_delete_venues] = mock_verify_dependency

    response = await test_app.delete(
        "/venue/266c40156f184248bbcb7fb70ba1ea90",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Failed to Delete, 266c4015-6f18-4248-bbcb-7fb70ba1ea90!"

    app.dependency_overrides.clear()
    