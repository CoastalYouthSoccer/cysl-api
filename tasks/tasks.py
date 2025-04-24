from datetime import datetime
import logging
from asyncio import run
from celery import Celery
import csv
from sqlalchemy import select
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session
from app.models.game import Game
from app.models.season import Season
from app.models.age_group import AgeGroup
from app.models.division import Division
from app.models.venue import Venue
from app.models.sub_venue import SubVenue
from app.config import get_settings

logger = logging.getLogger(__name__)

config = get_settings()

engine = create_engine(config.celery_database_url)

app = Celery()
app.config_from_object('celery_config')

def get_season_id(name, session: Session):
    result = session.exec(select(Season.id)
                          .where(Season.name == name))
    temp = result.first()

    if temp is None:
        logger.error(f'Invalid Season: {name}')
        return None
    return temp.id  

def get_division_id(name, session: Session):
    result = session.exec(select(Division.id)
                           .where(Division.name == name))
    temp = result.first()
    if temp is None:
        logger.error(f'Invalid Division: {name}')
        return None
    return temp.id  

def get_age_group_id(name, session: Session):
    result = session.exec(select(AgeGroup.id)
                           .where(AgeGroup.name == name))
    temp = result.first()
    if temp is None:
        logger.error(f'Invalid Age/Group: {name}')
        return None
    return temp.id

def get_venue_id(name, session: Session):
    result = session.exec(select(Venue.id)
                           .where(Venue.name == name))
    temp = result.first()
    if temp is None:
        logger.error(f'Invalid Venue: {name}')
        return None
    return temp.id

def get_sub_venue_id(name, venue_id, session: Session):
    result = session.exec(select(SubVenue.id)
                           .where(SubVenue.venue_id == venue_id)
                           .where(SubVenue.name == name))
    temp = result.first()
    if temp is None:
        logger.error(f'Invalid Sub-Venue: {name}')
        return None
    return temp.id

def set_game_dt(game_date, game_time):
    try:
        if game_time:
            return datetime.strptime(f"{game_date} {game_time}",
                                     "%m/%d/%Y %H:%M:%S")
        else:
            return datetime.strptime(f"{game_date}", "%m/%d/%Y")
    except Exception:
        logger.error(f'Invalid date and time: {game_date} , {game_time}')
        return None

def set_gender_boy(value):
    if 'boy' in value.lower():
        return 1
    else:
        return 0

def check_game_exists(season_id, division_id, age_group_id, gender,
                     game_dt, home_team, away_team, sub_venue_id,
                     session: Session):
    result = session.exec(select(Game.id)
                           .where(Game.season_id == season_id)
                           .where(Game.division_id == division_id)
                           .where(Game.age_group_id == age_group_id)
                           .where(Game.gender_boy == gender)
                           .where(Game.game_dt == game_dt)
                           .where(Game.home_team == home_team)
                           .where(Game.away_team == away_team)
                           .where(Game.sub_venue_id == sub_venue_id)
                           )
    temp = result.first()
    if temp:
        logger.warning(f'Game Already Exists: {temp.id}')
        return True
    return False
    
@app.task
def upload_schedule(season, filename):
    with Session(engine) as session:
        season_id = get_season_id(season, session)
        if season_id is None:
            logger.fatal(f'Invalid Season: {season} ... Exiting')
            return False

        with open(filename, mode="r", newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)     # Skip the titles
            for row in csv_reader:
                division_id = get_division_id(row[0], session)
                age_group_id = get_age_group_id(row[1], session)
                gender = set_gender_boy(row[2])
                game_dt = set_game_dt(row[3], row[4])
                venue_id = get_venue_id(row[7], session)
                if venue_id:
                    sub_venue_id = get_sub_venue_id(row[8], venue_id,
                                                    session)
                else:
                    sub_venue_id = None
                # Check if game exists
                if not check_game_exists(season_id, division_id,
                                        age_group_id, gender,
                                        game_dt, row[5], row[6],
                                        sub_venue_id, session):
                    game = Game(season_id=season_id,
                                division_id=division_id,
                                age_group_id=age_group_id,
                                gender_boy=gender,
                                game_dt=game_dt,
                                home_team=row[5], away_team=row[6],
                                sub_venue_id=sub_venue_id
                                )
                    session.add(game)
                    session.commit()
