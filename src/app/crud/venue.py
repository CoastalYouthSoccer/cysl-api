import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from pydantic import UUID4
from app.models import Venue as VenueModel
from app.schemas import Venue
logger = logging.getLogger(__name__)

async def get_Venues(session: AsyncSession, skip: int=0, limit: int=100):
    result = await session.execute(select(VenueModel).where(VenueModel.active == True). \
        limit(limit=limit).offset(offset=skip))
    return result.scalars().all()

async def get_Venue_by_name(session: AsyncSession, name: str):
    return await session.execute(select(VenueModel). \
                      where(VenueModel.name == name)).all()

async def get_Venue_by_association(session: AsyncSession, id: UUID4):
    return await session.execute(select(VenueModel). \
                      where(VenueModel.association_id == id)).all()

async def deactivate_Venue(session: AsyncSession, id: UUID4):
    try:
        temp = await session.get(VenueModel, id)
        if temp:
            await session.execute(
                update(VenueModel), [{"id": id, "active": False}]
                )
        else:
            msg = f"Venue, {temp.name}, doesn't exists!"
            logger.info(msg)
            raise HTTPException(status_code=400, detail=msg)
    except Exception as e:
        logger.error(e)
        return True
    
    return False

async def create_Venue(session: AsyncSession, item: Venue):
    temp = await get_Venue_by_name(session, name=item.name)
    if temp:
        msg = f"Venue, {item.name}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)

    active = True if item.active is None else item.active
    db_item = VenueModel(name=item.name, start_dt=item.start_dt,
                            end_dt=item.end_dt, active=active)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
