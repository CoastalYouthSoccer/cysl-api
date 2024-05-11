from datetime import datetime, date
from uuid import uuid4
from typing import Optional
from sqlalchemy.sql import expression

from sqlmodel import SQLModel, Field


class SeasonBase(SQLModel):
    name: str
    start_dt: date
    end_dt: date
    active: bool


class Season(SeasonBase, table=True):
    __tablename__: str = 'season'
    id: uuid4 = Field(primary_key=True, default=uuid4)


class SeasonCreate(SeasonBase):
    pass


class MisconductBase(SQLModel):
    game_dt: datetime
    venue: str
    age_group: str
    gender: str
    home_team: str
    home_team_coach: str
    home_score: int
    away_team: str
    away_team_coach: str
    away_score: int
    reported_by: str
    referee: str
    ar1: Optional[str]
    ar2: Optional[str]
    code: str
    offender_name: str
    coach_player: str
    player_nbr: str
    offender_team: str
    minute: int
    offense: str
    description: str

class Misconduct(MisconductBase, table=True):
    __tablename__: str = 'misconduct'
    id: uuid4 = Field(primary_key=True, default=uuid4)


class MisconductCreate(MisconductBase):
    pass

