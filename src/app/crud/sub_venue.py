import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from sqlalchemy.orm import selectinload

from pydantic import UUID4
from app.models import SubVenue as SubVenueModel
from app.schemas import SubVenueCreate, SubVenue, SubVenueUpdate

logger = logging.getLogger(__name__)

async def get_sub_venues(session: AsyncSession, skip: int=0, limit: int=100,
                           name: str=None, venue_id: UUID4=None):
    if name:
        result = await get_sub_venue_by_name(session=session,
                                        name=name)
        if result:
            return [result]
        else:
            msg = f"Venue, {name}, Not Found"
            logger.debug(msg)
            raise HTTPException(status_code=404, detail=msg)

    if venue_id:
        result = await session.execute(
            select(SubVenueModel).where(SubVenueModel.active == True). \
            where(SubVenueModel.venue_id == venue_id). \
            limit(limit=limit).offset(offset=skip))
        sub_venues = result.scalars().all()
        return [SubVenue.model_validate(sub_venue) for sub_venue in sub_venues]


    result = await session.execute(
        select(SubVenueModel).where(SubVenueModel.active == True). \
        limit(limit=limit).offset(offset=skip))
    sub_venues = result.scalars().all()
    return [SubVenue.model_validate(sub_venue) for sub_venue in sub_venues]

async def get_sub_venue_by_name(session: AsyncSession, name: str):
    result = await session.execute(select(SubVenueModel). \
                    where(SubVenueModel.name == name))
    return result.scalar_one_or_none()

async def get_sub_venue_by_id(session: AsyncSession, id: UUID4):
    temp = await session.execute(select(SubVenueModel). \
                      options(
                        selectinload(SubVenueModel.address),
                        selectinload(SubVenueModel.association)
                    ).where(SubVenueModel.id == id))
    result = temp.scalar_one_or_none()
    if result:
        return result
    msg = f"Sub-Venue, {id}, Not Found"
    logger.debug(msg)
    raise HTTPException(status_code=404, detail=msg)

async def deactivate_sub_venue(session: AsyncSession, id: UUID4):
    try:
        temp = await session.get(SubVenueModel, id)
        if temp:
            await session.execute(
                update(SubVenueModel), [{"id": id, "active": False}]
                )
        else:
            msg = f"Venue, {temp.name}, doesn't exists!"
            logger.info(msg)
            raise HTTPException(status_code=404, detail=msg)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404,
                            detail=f"Failed to Delete, {id}!")
    
async def create_sub_venue(session: AsyncSession, item: SubVenueCreate):
    temp = await get_sub_venue_by_name(session, name=item.name)
    if temp:
        msg = f"Venue, {item.name}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=409, detail=msg)

    active = True if item.active is None else item.active
    db_item = SubVenueModel(name=item.name, active=active,
                         venue_id=item.venue_id)
    try:
        session.add(db_item)
        await session.commit()
    except Exception as e:
        logger.error(f"Unable to create Sub-Venue, {item.name}: {e}")
        await session.rollback()
    await session.refresh(db_item)
    return db_item

async def update_sub_venue(session: AsyncSession, item: SubVenueUpdate):
    sub_venue = await session.get(SubVenueModel, item.id)
    if not sub_venue:
        msg = f"Sub-Venue not found: {item.name}"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)

    active = True if item.active is None else item.active
    sub_venue.name = item.name
    sub_venue.active = active
    sub_venue.venue_id = item.venue_id

    session.add(sub_venue)
    await session.commit()
    await session.refresh(sub_venue)
    return sub_venue
