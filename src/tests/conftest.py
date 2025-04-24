from os import environ, getenv
from dotenv import load_dotenv
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
from app.database import async_engine

load_dotenv(dotenv_path=".test.env", override=True)

from app.database import get_session
from main import app

seed_info = {
    "season": Season, "misconduct": Misconduct,
    "association": Association
}

@pytest.fixture(scope='session')
def test_client():
    client = TestClient(app)
    yield client

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
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
