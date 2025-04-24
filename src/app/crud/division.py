import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from pydantic import UUID4
from app.models import Division as DivisionModel
from app.schemas import DivisionCreate
logger = logging.getLogger(__name__)

async def get_divisions(session: AsyncSession, skip: int=0, limit: int=100,
                           name: str=None):
    if name:
        result = await get_division_by_name(session=session,
                                        name=name)
        if result:
            return [result]
        else:
            msg = f"Division, {name} Not Found"
            logger.debug(msg)
            raise HTTPException(status_code=404, detail=msg)
    else:
        result = await session.execute(select(DivisionModel).where(DivisionModel.active == True). \
            limit(limit=limit).offset(offset=skip))
        return result.scalars().all()

async def get_division_by_name(session: AsyncSession, name: str):
    result = await session.execute(select(DivisionModel). \
                      where(DivisionModel.name == name))
    return result.scalar_one_or_none()

async def get_division_by_id(session: AsyncSession, id: UUID4):
    result = await session.get(DivisionModel, id)
    if not result:
        msg = f"Division, {id} Not Found"
        logger.debug(msg)
        raise HTTPException(status_code=404, detail=msg)
    return result

async def deactivate_division(session: AsyncSession, id: UUID4):
    try:
        temp = await session.get(DivisionModel, id)
        if temp:
            await session.execute(
                update(DivisionModel), [{"id": id, "active": False}]
                )
        else:
            msg = f"Division, {temp.name}, doesn't exists!"
            logger.info(msg)
            raise HTTPException(status_code=404, detail=msg)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404,
                            detail=f"Failed to Delete, {id}!")
    
async def create_division(session: AsyncSession, item: DivisionCreate):
    temp = await get_division_by_name(session, name=item.name)
    if temp:
        msg = f"Division, {item.name}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)

    active = True if item.active is None else item.active
    db_item = DivisionModel(name=item.name, active=active)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
