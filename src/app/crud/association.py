import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from pydantic import UUID4
from app.models import Association as AssociationModel
from app.schemas import AssociationCreate
logger = logging.getLogger(__name__)

async def get_associations(session: AsyncSession, skip: int=0, limit: int=100):
    result = await session.execute(select(AssociationModel).where(AssociationModel.active == True). \
        limit(limit=limit).offset(offset=skip))
    return result.scalars().all()

async def get_association_by_name(session: AsyncSession, name: str):
    return await session.execute(select(AssociationModel). \
                      where(AssociationModel.name == name)).all()

async def deactivate_association(session: AsyncSession, id: UUID4):
    try:
        temp = await session.get(AssociationModel, id)
        if temp:
            msg = f"Association, {temp.name}, already exists!"
            logger.info(msg)
            raise HTTPException(status_code=400, detail=msg)
        await session.execute(
            update(AssociationModel), [{"id": id, "active": False}]
        )
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
    db_item = AssociationModel(name=item.name, start_dt=item.start_dt,
                            end_dt=item.end_dt, active=active)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
