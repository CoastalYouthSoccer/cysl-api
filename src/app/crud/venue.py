import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from sqlalchemy.orm import selectinload

from pydantic import UUID4
from app.models import Venue as VenueModel
from app.models import Association as AssociationModel
from app.models import Address as AddressModel
from app.schemas import VenueCreate, Venue
from .address import read_create_address
from .association import get_association_by_id

logger = logging.getLogger(__name__)

async def get_venues(session: AsyncSession, skip: int=0, limit: int=100,
                           name: str=None, association: str=None,
                           association_id: UUID4=None):
    if name:
        result = await get_venue_by_name(session=session,
                                        name=name)
        if result:
            return [result]
        else:
            msg = f"Venue, {name}, Not Found"
            logger.debug(msg)
            raise HTTPException(status_code=404, detail=msg)

    if association:
        return await get_venues_by_association(session=session,
                                        name=association)

    if association_id:
        return await get_venues_by_association_id(session=session,
                                        id=association_id)

    result = await session.execute(
        select(VenueModel).where(VenueModel.active == True). \
        limit(limit=limit).offset(offset=skip) . \
        options(
            selectinload(VenueModel.address),
            selectinload(VenueModel.association),
        )
    )
    venues = result.scalars().all()
    return [Venue.model_validate(venue) for venue in venues]

async def get_venue_by_name(session: AsyncSession, name: str):
    result = await session.execute(select(VenueModel). \
                      options(
                        selectinload(VenueModel.address),
                        selectinload(VenueModel.association)
                    ).where(VenueModel.name == name))
    return result.scalar_one_or_none()

async def get_venues_by_association(session: AsyncSession, name: str):
    temp = await session.execute(select(AssociationModel). \
                                 where(AssociationModel.name == name))
    result = temp.scalar_one_or_none()
    if result:
        return await get_venues_by_association_id(session, result.id)
    else:
        msg = f"Searching Venues for non-existing Association, {name}"
        logger.debug(msg)
        raise HTTPException(status_code=404, detail=msg)

async def get_venues_by_association_id(session: AsyncSession, id: UUID4):
    result = await session.execute(select(VenueModel). \
                      where(VenueModel.association_id == id). \
                      options(
                        selectinload(VenueModel.address),
                        selectinload(VenueModel.association),
                    ))
    return result.scalars().all()

async def get_venue_by_id(session: AsyncSession, id: UUID4):
    temp = await session.execute(select(VenueModel). \
                      options(
                        selectinload(VenueModel.address),
                        selectinload(VenueModel.association)
                    ).where(VenueModel.id == id))
    result = temp.scalar_one_or_none()
    if result:
        return result
    msg = f"Venue, {id}, Not Found"
    logger.debug(msg)
    raise HTTPException(status_code=404, detail=msg)

async def deactivate_venue(session: AsyncSession, id: UUID4):
    try:
        temp = await session.get(VenueModel, id)
        if temp:
            await session.execute(
                update(VenueModel), [{"id": id, "active": False}]
                )
        else:
            msg = f"Venue, {temp.name}, doesn't exists!"
            logger.info(msg)
            raise HTTPException(status_code=404, detail=msg)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404,
                            detail=f"Failed to Delete, {id}!")
    
async def create_venue(session: AsyncSession, item: VenueCreate):
    temp = await get_venue_by_name(session, name=item.name)
    if temp:
        msg = f"Venue, {item.name}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=409, detail=msg)

    _ = await get_association_by_id(session,
                                    id=item.association.id)
    address = await read_create_address(session, address=item.address)
    active = True if item.active is None else item.active
    db_item = VenueModel(name=item.name, active=active,
                         address_id=address.id,
                         association_id=item.association.id)
    try:
        session.add(db_item)
        await session.commit()
    except Exception as e:
        logger.error(f"Unable to create Venue, {item.name}: {e}")
        await session.rollback()
    await session.refresh(db_item)
    return db_item

async def update_venue(session: AsyncSession, item: Venue):
    venue = await session.get(VenueModel, item.id)
    if not venue:
        msg = f"Venue not found: {item.name}"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)
    
    if item.name is not None:
        venue.name = item.name

    if item.address:
        address_data = item.address.dict(exclude_unset=True)
        address_id = address_data.get("id")

        address = await session.get(AddressModel, address_id) if address_id else None

        if address:
            for field, value in address_data.items():
                if field != "id":
                    setattr(address, field, value)
        else:
            new_address = AddressModel(**address_data)
            session.add(new_address)
            await session.flush() 
            venue.address_id = new_address.id
        if address:
            venue.address_id = address.id

    session.add(venue)
    await session.commit()
    await session.refresh(venue)
    return venue
