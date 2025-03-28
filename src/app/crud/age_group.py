import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import AgeGroup as AgeGroupModel
logger = logging.getLogger(__name__)

async def get_age_groups(session: AsyncSession, skip: int=0, limit: int=100):
    result = await session.execute(select(AgeGroupModel). \
        limit(limit=limit).offset(offset=skip))
    return result.scalars().all()
