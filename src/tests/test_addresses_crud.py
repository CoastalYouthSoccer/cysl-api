import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, and_
from pydantic import UUID4
from app.models import Address as AddressModel
from app.schemas import AddressCreate
logger = logging.getLogger(__name__)

async def read_create_address(session:AsyncSession, address: AddressCreate):
    conditions = [
        AddressModel.address1 == address.address1,
        AddressModel.city == address.city,
        AddressModel.zip_code == address.zip_code
    ]

    if address.address2 is not None:
        conditions.append(AddressModel.address2 == address.address2)

    temp = await session.execute(select(AddressModel).where(
        and_(*conditions))
    )

    result = temp.scalar_one_or_none()
    if result:
        return result
    
    active = True if address.active is None else address.active
    db_item = AddressModel(address1=address.address1, active=active,
                           address2=address.address2, city=address.city,
                           zip_code=address.zip_code, state=address.state)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

async def get_address_by_id(session: AsyncSession, id: UUID4):
    result = await session.get(AddressModel, id)
    if not result:
        msg = f"Address, {id}, Not Found"
        logger.debug(msg)
        raise HTTPException(status_code=404, detail=msg)
    return result

async def deactivate_address(session: AsyncSession, id: UUID4):
    try:
        temp = await session.get(AddressModel, id)
        if temp:
            await session.execute(
                update(AddressModel), [{"id": id, "active": False}]
                )
        else:
            msg = f"Address, {temp.name}, doesn't exists!"
            logger.info(msg)
            raise HTTPException(status_code=404, detail=msg)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404,
                            detail=f"Failed to Delete, {id}!")
