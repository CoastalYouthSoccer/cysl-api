from datetime import datetime
import uuid

from typing import Optional

from sqlmodel import SQLModel, Field


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
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class MisconductCreate(MisconductBase):
    pass