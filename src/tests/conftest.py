from os import getenv
import asyncio
import pytest
import jwt
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI

from httpx import AsyncClient

from os.path import (join, abspath, dirname)
import json
from sqlalchemy import insert, MetaData

from app.models import (Season, Misconduct, Association)
#from app.database import init_db, get_session
from main import app

seed_info = {
    "season": Season, "misconduct": Misconduct,
    "association": Association
}

engine = AsyncEngine(create_engine(getenv("DATABASE_URL"), echo=True, future=True))

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting up")
    yield
    print("shutting down")

# drop all database every time when test complete
@pytest.fixture(scope='session')
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

# truncate all table to isolate tests
@pytest.fixture(scope='function')
async def async_db(async_db_engine):
    async_session = sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()

        for table in reversed(SQLModel.metadata.sorted_tables):
            await session.execute(f'TRUNCATE {table.name} CASCADE;')
            await session.commit()

@pytest.fixture(scope='session')
async def async_client() -> AsyncClient:
    async with lifespan(app):
        async with AsyncClient as async_client:
            yield async_client

@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

def mock_auth0_token(permissions=[]):
    secret_key = 'your-secret-key'

    payload = {
        "iss": "https://test-auth0-domain.auth0.com/",
        "sub": "auth0|1234567890",
        "aud": ["your-client-id", "https://test-api-endpoint.com"],
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow(),
        "name": "John Doe",
        "email": "john.doe@example.com",
        "permissions": permissions
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def load_database(db_session, file_name, data_model):
    with open(file_name) as f_in:
        data = json.load(f_in)
        db_session.execute(insert(data_model), data)

#@pytest.fixture(scope='class', autouse=True)
#async def init_database(request):
#    """Initializes the database """
#    db = get_session()
#    await init_db()
#
#    base_dir = join(abspath(dirname(__file__)))
#
#    for file_name, model_name in seed_info.items():
#        temp_name = join(base_dir, 'seed', f"{file_name}.json")
#        load_database(db, temp_name, model_name)
#
#    request.cls.db = db
#    yield
#    db.close()


#@pytest.fixture(scope='session')
#def event_loop():
#    """Override the default event loop for pytest-asyncio."""
#    loop = get_event_loop()
#    yield loop
#    loop.close()
