import logging
from urllib.parse import urlparse, quote_plus, urlunparse

from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from app.config import get_settings
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

config = get_settings()
parsed = urlparse(config.database_url.strip('"').strip("'"))

# Encode just the password
encoded_password = quote_plus(parsed.password) if parsed.password else ''

# Rebuild the URL with encoded password
database_url = f"{parsed.scheme}://{parsed.username}:{encoded_password}@{parsed.hostname}"
if parsed.port:
    database_url += f":{parsed.port}"
database_url += parsed.path

print(f"DEBUG: Database URL: {database_url}")
async_engine = AsyncEngine(create_engine(config.database_url, echo=True, future=True))

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session() as session:
        yield session
