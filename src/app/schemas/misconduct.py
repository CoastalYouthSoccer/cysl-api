from datetime import datetime
from .base import Base, BaseCreate
from pydantic import ConfigDict


class Misconduct(Base):
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
    ar1: str
    ar2: str
    result: str
    offender_name: str
    coach_player: str
    player_nbr: str
    offender_team: str
    minute: int
    offense: str
    description: str

    model_config = ConfigDict(
        from_attributes=True
    )


class MisconductCreate(BaseCreate):
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
    ar1: str
    ar2: str
    result: str
    offender_name: str
    coach_player: str
    player_nbr: str
    offender_team: str
    minute: int
    offense: str
    description: str

    model_config = ConfigDict(
        from_attributes=True
    )
