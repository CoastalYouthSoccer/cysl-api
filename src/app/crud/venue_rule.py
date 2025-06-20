import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, and_
from pydantic import UUID4
from app.models import VenueRule as VenueRuleModel
from app.schemas import VenueRuleCreate, VenueRule

logger = logging.getLogger(__name__)

async def get_venue_rules(session: AsyncSession, skip: int=0, limit: int=100):
    result = await session.execute(select(VenueRuleModel).where(VenueRuleModel.active == True). \
        limit(limit=limit).offset(offset=skip))
    return result.scalars().all()

async def get_venue_rule_by_id(session: AsyncSession, id: UUID4):
    result = await session.get(VenueRuleModel, id)
    if not result:
        msg = f"Venue Rule, {id}, Not Found"
        logger.debug(msg)
        raise HTTPException(status_code=404, detail=msg)
    return result

async def deactivate_venue_rule(session: AsyncSession, id: UUID4):
    try:
        temp = await session.get(VenueRuleModel, id)
        if temp:
            await session.execute(
                update(VenueRuleModel), [{"id": id, "active": False}]
                )
        else:
            msg = f"VenueRule, {temp.name}, doesn't exists!"
            logger.info(msg)
            raise HTTPException(status_code=404, detail=msg)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404,
                            detail=f"Failed to Delete, {id}!")
    
async def create_venue_rule(session: AsyncSession, item: VenueRuleCreate):
    temp = await session.execute(select(VenueRuleModel). \
                      where(VenueRuleModel.association_id == item.association_id,
                            VenueRuleModel.age_group_id == item.age_group_id,
                            VenueRuleModel.gender_boy == item.gender_boy,
                            VenueRuleModel.division_id == item.division_id)).all()
    if temp:
        msg = f"VenueRule already exists!"
        logger.info(msg)
        raise HTTPException(status_code=409, detail=msg)

    active = True if item.active is None else item.active
    db_item = VenueRuleModel(association_id=item.association_id, active=active,
                             age_group_id=item.age_group_id,
                             gender_boy=item.gender_boy,
                             division_id=item.division_id, venue=item.venue,
                             sub_venue=item.sub_venue)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

async def update_venue_rule(session: AsyncSession, item: VenueRule):
    venue_rule = await session.get(VenueRuleModel, item.id)
    if not venue_rule:
        msg = f"Venue Rule not found: {item.id}"
        logger.warning(msg)
        raise HTTPException(status_code=404, detail=msg)
    
    venue_rule.association_id = item.association_id
    venue_rule.age_group_id = item.age_group_id
    venue_rule.gender_boy = item.gender_boy
    venue_rule.division_id = item.division_id
    venue_rule.venue = item.venue
    venue_rule.sub_venue = item.sub_venue

    session.add(venue_rule)
    await session.commit()
    await session.refresh(venue_rule)
    return venue_rule