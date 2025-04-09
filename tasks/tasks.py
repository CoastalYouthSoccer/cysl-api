from datetime import datetime
import logging
from asyncio import run
from celery import Celery
import csv
from sqlalchemy import select
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from app.models.game import Game
from app.models.season import Season
from app.models.age_group import AgeGroup
from app.models.division import Division
from app.models.venue import Venue
from app.models.sub_venue import SubVenue
from app.config import get_settings

logger = logging.getLogger(__name__)

config = get_settings()

async_engine = AsyncEngine(create_engine(config.database_url, echo=True, future=True))

@asynccontextmanager
async def get_session() -> AsyncSession:
    session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session() as session:
        yield session

app = Celery()
app.config_from_object('celery_config')

async def get_season_id(name, session: AsyncSession):
    result = await session.execute(select(Season.id)
                          .where(Season.name == name))
    temp = result.first()
    if temp is None:
        logger.error(f'Invalid Season: {name}')
        return None
    return temp.id  

async def get_division_id(name, session: AsyncSession):
    result = await session.execute(select(Division.id)
                           .where(Division.name == name))
    temp = result.first()
    if temp is None:
        logger.error(f'Invalid Division: {name}')
        return None
    return temp.id  

async def get_age_group_id(name, session: AsyncSession):
    result = await session.execute(select(AgeGroup.id)
                           .where(AgeGroup.name == name))
    temp = result.first()
    if temp is None:
        logger.error(f'Invalid Age/Group: {name}')
        return None
    return temp.id

async def get_venue_id(name, session: AsyncSession):
    result = await session.execute(select(Venue.id)
                           .where(Venue.name == name))
    temp = result.first()
    if temp is None:
        logger.error(f'Invalid Venue: {name}')
        return None
    return temp.id

async def get_sub_venue_id(name, venue_id, session: AsyncSession):
    result = await session.execute(select(SubVenue.id)
                           .where(SubVenue.venue_id == venue_id)
                           .where(SubVenue.name == name))
    temp = result.first()
    if temp is None:
        logger.error(f'Invalid Sub-Venue: {name}')
        return None
    return temp.id

def set_game_dt(game_date, game_time):
    try:
        return datetime.strptime(f"{game_date} {game_time}",
                                 "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.error(f'Invalid date and time: {game_date} , {game_time}')
        return None

def set_gender_boy(value):
    if 'boy' in value.lower():
        return 1
    else:
        return 0

@app.task
def upload_schedule(season, filename):
    return run(_upload_schedule(season, filename))

async def _upload_schedule(season, filename):
    async with get_session() as session:
        season_id = await get_season_id(season, session)
        if season_id is None:
            logger.fatal(f'Invalid Season: {season} ... Exiting')
            return False

        with open(filename, mode="r", newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)     # Skip the titles
            for row in csv_reader:
                division_id = await get_division_id(row[0], session)
                age_group_id = await get_age_group_id(row[1], session)
                venue_id = await get_venue_id(row[7], session)
                if venue_id:
                    sub_venue_id = await get_sub_venue_id(row[8], venue_id,
                                                    session)
                else:
                    sub_venue_id = None

                game = Game(season_id=season_id,
                            division_id=division_id,
                            age_group_id=age_group_id,
                            gender_boy=set_gender_boy(row[2]),
                            game_dt=set_game_dt(row[3], row[4]),
                            home_team=row[5], away_team=row[6],
                            sub_venue_id=sub_venue_id
                            )
                session.add(game)
