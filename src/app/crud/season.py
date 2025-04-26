import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from pydantic import UUID4
from app.models import Season as SeasonModel
from app.schemas import Season as SeasonCreate

logger = logging.getLogger(__name__)

async def get_seasons(session: AsyncSession, skip: int=0, limit: int=100,
                      name: str=None):
    if name:
        result = await get_season_by_name(session=session,
                                        name=name)
        if result:
            return [result]
        else:
            msg = f"Season, {name}, Not Found"
            logger.debug(msg)
            raise HTTPException(status_code=404, detail=msg)
    else:
        result = await session.execute(select(SeasonModel).where(SeasonModel.active == True). \
            limit(limit=limit).offset(offset=skip))
        return result.scalars().all()

async def get_season_by_name(session: AsyncSession, name: str):
    result = await session.execute(select(SeasonModel). \
                      where(SeasonModel.name == name))
    return result.scalar_one_or_none()

async def get_season_by_id(session: AsyncSession, id: UUID4):
    result = await session.get(SeasonModel, id)
    if not result:
        msg = f"Season, {id}, Not Found"
        logger.debug(msg)
        raise HTTPException(status_code=404, detail=msg)
    return result

async def deactivate_season(session: AsyncSession, id: UUID4):
    try:
        temp = await session.get(SeasonModel, id)
        if temp:
            _ = await session.execute(
                update(SeasonModel), [{"id": id, "active": False}]
            )
        else:
            msg = f"Season, {id}, doesn't exist!"
            logger.info(msg)
            raise HTTPException(status_code=404, detail=msg)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404,
                            detail=f"Failed to Delete, {id}!")

async def create_season(session: AsyncSession, item: SeasonCreate):
    temp = await get_season_by_name(session, name=item.name)
    if temp:
        msg = f"Season, {item.name}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=409, detail=msg)

    active = True if item.active is None else item.active
    db_item = SeasonModel(name=item.name, start_dt=item.start_dt,
                            season_length=item.season_length,
                            active=active,
                            holiday_dates=item.holiday_dates)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item
