import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from pydantic import UUID4
from app.models import Association as AssociationModel
from app.schemas import AssociationCreate
logger = logging.getLogger(__name__)

async def get_association(session: AsyncSession, id: UUID4):
    result = await session.get(AssociationModel, id)
    if not result:
        msg = f"Association, {id} Not Found"
        logger.debug(msg)
        raise HTTPException(status_code=404, detail=msg)
    return result

async def get_associations(session: AsyncSession, skip: int=0, limit: int=100,
                           name: str=None):
    if name:
        result = await get_association_by_name(session=session,
                                        name=name)
        if result:
            return [result]
        else:
            msg = f"Association, {name} Not Found"
            logger.debug(msg)
            raise HTTPException(status_code=404, detail=msg)
    else:
        result = await session.execute(select(AssociationModel).where(AssociationModel.active == True). \
            limit(limit=limit).offset(offset=skip))
        return result.scalars().all()

async def get_association_by_name(session: AsyncSession, name: str):
    result = await session.execute(select(AssociationModel). \
                      where(AssociationModel.name == name))
    return result.scalar_one_or_none()

async def deactivate_association(session: AsyncSession, id: UUID4):
    try:
        temp = await session.get(AssociationModel, id)
        if temp:
            await session.execute(
                update(AssociationModel), [{"id": id, "active": False}]
                )
        else:
            msg = f"Association, {temp.name}, doesn't exists!"
            logger.info(msg)
            raise HTTPException(status_code=400, detail=msg)
    except Exception as e:
        logger.error(e)
        return True
    
    return False

async def create_association(session: AsyncSession, item: AssociationCreate):
    temp = await get_association_by_name(session, name=item.name)
    if temp:
        msg = f"Association, {item.name}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)

    active = True if item.active is None else item.active
    db_item = AssociationModel(name=item.name, active=active)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
