import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy import update, select, delete
from pydantic import UUID4
from app.models import Game as GameModel
from app.schemas import Game  
logger = logging.getLogger(__name__)

async def get_game(session: AsyncSession, id: UUID4):
    result = await session.execute(select(GameModel). \
                    where(GameModel.id == id))
    game = result.scalar_one_or_none()
    if game is None:
        msg = f"Unable to find Game, {id}"
        raise HTTPException(status_code=404, detail=msg)

    return game

async def get_games(session: AsyncSession, skip: int=0, limit: int=100):
    result = await session.execute(select(GameModel). \
        limit(limit=limit).offset(offset=skip))
    return result.scalars().all()

async def check_for_existing_game(session: AsyncSession, item: Game):
    return await session.execute(select(GameModel). \
                      where(GameModel.season_id == item.season_id,
                            GameModel.age_group_id == item.age_group_id,
                            GameModel.gender_boy == item.gender_boy,
                            GameModel.away_team == item.away_team,
                            GameModel.division_id == item.division_id,
                            GameModel.game_dt == item.game_dt,
                            GameModel.home_team == item.home_team,
                            GameModel.sub_venue_id == item.sub_venue_id)).all()

async def create_game(session: AsyncSession, item: Game):
    temp = await check_for_existing_game(session, item=item)
    if temp:
        msg = f"Game, {temp.id}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)

    db_item = GameModel(season_id=item.season_id, division_id=item.division_id,
                        age_group_id=item.age_group_id, home_team=item.home_team,
                        game_dt=item.game_dt, away_team=item.away_team,
                        sub_venue_id=item.sub_venue_id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

async def delete_game(session: AsyncSession, id: UUID4):
    try:
        await session.execute(delete(GameModel).where(GameModel.id == id))
        msg = f"Game id: {id} deleted!"
        logger.info(msg)
        return False
    except Exception as e:
        logger.error(e)
        msg = f"Failed to delete game with id {id}."
        raise HTTPException(status_code=400, detail=msg)

async def update_game(session: AsyncSession, item: Game, id: UUID4):
    temp = await session.get(Game, id)
    if temp:
        try:
            await session.execute(
                update(GameModel), [{"id": id, "season_id": item.season_id,
                                    "division_id": item.division_id,
                                    "age_group_id": item.age_group_id,
                                    "home_team": item.home_team,
                                    "game_dt": item.game_dt,
                                    "away_team": item.away_team,
                                    "sub_venue_id": item.sub_venue_id,
                                    "home_score": item.home_score,
                                    "away_score": item.away_score}]
            )
        except Exception as e:
            logger.error(e)
            msg = f"Unable to update Game, {temp.id}"
            raise HTTPException(status_code=400, detail=msg)
    else:
        msg = f"Game, {temp.id}, doesn't exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)
    
    return False
