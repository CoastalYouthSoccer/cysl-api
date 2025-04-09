import logging

from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from app.config import get_settings
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

config = get_settings()

async_engine = AsyncEngine(create_engine(config.database_url, echo=True, future=True))

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

@asynccontextmanager
async def get_session() -> AsyncSession:
    session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session() as session:
        yield session
