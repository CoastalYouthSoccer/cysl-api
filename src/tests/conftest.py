from os import getenv
import asyncio
import pytest
import jwt
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Security, Depends
from fastapi.security import SecurityScopes
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock

from os.path import (join, abspath, dirname)
import json
from sqlalchemy import insert, MetaData
from fastapi.testclient import TestClient

from app.models import (Season, Misconduct, Association)
from app.dependencies import auth


from app.database import get_session
from main import app
from app.config import get_settings

config = get_settings()

seed_info = {
    "season": Season, "misconduct": Misconduct,
    "association": Association
}

async def override_auth_verify(security_scopes: SecurityScopes, token: str = Depends()):
    return {
        "sub": "auth0|test-user",
        "permissions": security_scopes.scopes
    }

async_engine = AsyncEngine(create_engine(getenv("DATABASE_URL"), echo=True, future=True))

@pytest.fixture
def mock_session():
    mock = AsyncMock()
    return mock

@pytest.fixture(autouse=True)
def override_get_session(mock_session):
    app.dependency_overrides[get_session] = lambda: mock_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope='session')
def test_client():
    client = TestClient(app)
    yield client

@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture(scope="module")
async def test_app():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,
                            base_url="http://test") as client:
        yield client

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting up")
    yield
    print("shutting down")

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="module")
def mock_auth0_token():
    def generate_token(permissions=[]):
        payload = {
            "iss": "https://your-issuer/",
            "sub": "auth0|test",
            "aud": "your-audience",
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "permissions": permissions
        }
        token = jwt.encode(payload, "your-secret-key", algorithm="HS256")
        return token
    return generate_token

@pytest.fixture(autouse=True, scope="module")
def override_auth():
    app.dependency_overrides[auth] = override_auth_verify
    yield
    app.dependency_overrides.pop(auth, None)
