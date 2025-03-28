import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete
from pydantic import UUID4
from app.models import Game as GameModel
from app.schemas import GameCreate
logger = logging.getLogger(__name__)

async def get_games(session: AsyncSession, skip: int=0, limit: int=100):
    result = await session.execute(select(GameModel). \
        limit(limit=limit).offset(offset=skip))
    return result.scalars().all()

async def get_game_by_name(session: AsyncSession, name: str):
    return await session.execute(select(GameModel). \
                      where(GameModel.name == name)).all()

async def create_game(session: AsyncSession, item: GameCreate):
    temp = await get_game_by_name(session, name=item.name)
    if temp:
        msg = f"Game, {item.name}, already exists!"
        logger.info(msg)
        raise HTTPException(status_code=400, detail=msg)

    active = True if item.active is None else item.active
    db_item = GameModel(name=item.name, start_dt=item.start_dt,
                            end_dt=item.end_dt, active=active)
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
