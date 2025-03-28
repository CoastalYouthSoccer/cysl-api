from datetime import datetime
import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from pydantic import UUID4
from app.models import (Misconduct as MisconductModel)
from app.schemas import Misconduct

logger = logging.getLogger(__name__)

async def get_misconducts(session: AsyncSession, skip: int=0, limit: int=100):
    result = await session.execute(select(MisconductModel). \
        limit(limit=limit).offset(offset=skip))
    return result.scalars().all()

async def check_misconduct_exists(session: AsyncSession, game_dt: datetime,
                            venue: str, age_group: str, gender: str,
                            home_team: str, away_team: str):
    return await session.execute(select(MisconductModel). \
                      where(MisconductModel.game_dt == game_dt). \
                      where(MisconductModel.age_group == age_group). \
                      where(MisconductModel.venue == venue). \
                      where(MisconductModel.gender == gender). \
                      where(MisconductModel.home_team == home_team). \
                      where(MisconductModel.away_team == away_team)).all()

async def deactivate_misconduct(session: AsyncSession, id: UUID4):
    temp = await session.get(Misconduct, id)
    if temp:
        try:
            await session.execute(
                update(MisconductModel), [{"id": id, "active": False}]
            )
        except Exception as e:
            logger.error(e)
            msg = f"Unable to update Misconduct, {temp.name}"
            raise HTTPException(status_code=400, detail=msg)
    else:
        msg = f"Misconduct, {temp.name}, doesn't exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)
    
    return False

async def create_misconduct(session: AsyncSession, item: Misconduct):
    temp = await check_misconduct_exists(session, game_dt=item.game_dt, venue=item.venue,
                                   age_group=item.age_group, gender=item.gender,
                                   home_team=item.home_team, away_team=item.away_team)
    if temp:
        msg = "Misconduct already exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)
    db_item = MisconductModel(game_dt=item.game_dt, venue=item.venue,
                              age_group=item.age_group, gender=item.gender,
                              home_team=item.home_team, away_team=item.away_team,
                              home_team_coach=item.home_team_coach,
                              away_team_coach=item.away_team_coach,
                              coach_player=item.coach_player,
                              home_score=item.home_score, away_score=item.away_score,
                              reported_by=item.reported_by, referee=item.referee,
                              ar1=item.ar1, ar2=item.ar2, result=item.result,
                              offender_name=item.offender_name,
                              player_nbr=item.player_nbr, offense=item.offense,
                              minute=item.minute, offender_team=item.offender_team,
                              description=item.description)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
