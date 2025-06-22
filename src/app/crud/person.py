import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, and_
from pydantic import UUID4
from app.models import Person as PersonModel
from app.schemas import PersonCreate, Person
from app.helpers.encrypt_decrypt import hmac_value

logger = logging.getLogger(__name__)

async def get_persons(session: AsyncSession, skip: int=0, limit: int=100,
                           first_name: str=None, last_name: str=None,
                           email: str=None):
    if first_name or last_name:
        result = await get_person_by_name(session=session,
                                        first_name=first_name,
                                        last_name=last_name)
        if result:
            return [result]
        else:
            msg = f"Person, { first_name} {last_name}, Not Found"
            logger.debug(msg)
            raise HTTPException(status_code=404, detail=msg)
    elif email:
        result = await get_person_by_email(session=session,
                                           email=email)
        if result:
            return [result]
        else:
            msg = f"Person with {email}, Not Found"
            logger.debug(msg)
            raise HTTPException(status_code=404, detail=msg)
    else:
        result = await session.execute(select(PersonModel).where(PersonModel.active == True). \
            limit(limit=limit).offset(offset=skip))
        return result.scalars().all()

async def get_person_by_name(session: AsyncSession, first_name: str,
                             last_name: str):
    filters = []
    if first_name:
        first_name_hash = hmac_value(first_name)
        filters.append(PersonModel.first_name_hmac == first_name_hash)

    if last_name:
        last_name_hash = hmac_value(last_name)
        filters.append(PersonModel.last_name_hmac == last_name_hash)

    if filters:
        result = await session.execute(
            select(PersonModel).where(and_(*filters))
        )
        return result.scalars().all()
    return []

async def get_person_by_id(session: AsyncSession, id: UUID4):
    result = await session.get(PersonModel, id)
    if not result:
        msg = f"Person, {id}, Not Found"
        logger.debug(msg)
        raise HTTPException(status_code=404, detail=msg)
    return result

async def get_person_by_email(session: AsyncSession, email: str):
    email_hash = hmac_value(email)

    result = await session.execute(select(PersonModel). \
                      where(PersonModel.email_hmac == email_hash))
    return result.scalar_one_or_none()

async def deactivate_person(session: AsyncSession, id: UUID4):
    try:
        temp = await session.get(PersonModel, id)
        if temp:
            await session.execute(
                update(PersonModel), [{"id": id, "active": False}]
                )
        else:
            msg = f"Person, {temp.name}, doesn't exists!"
            logger.info(msg)
            raise HTTPException(status_code=404, detail=msg)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404,
                            detail=f"Failed to Delete, {id}!")
    
async def create_person(session: AsyncSession, item: PersonCreate):
    temp = await get_person_by_email(session, email=item.email)
    if temp:
        msg = f"Person with, {item.email}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=409, detail=msg)

    active = True if item.active is None else item.active
    db_item = PersonModel(last_name=item.last_name, active=active,
                          first_name=item.first_name,
                          email=item.email)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

async def update_person(session: AsyncSession, item: Person):
    person = await session.get(PersonModel, item.id)
    if not person:
        msg = f"Person not found: {item.first_name} {item.last_name}"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)
    
    person.first_name = item.first_name
    person.last_name = item.last_name
    person.email = item.email

    session.add(person)
    await session.commit()
    await session.refresh(person)
    return person
