from enum import Enum
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, StringConstraints, UUID4
from typing_extensions import Annotated

#from pydantic_extra_types import phone_numbers


class GameStatus(Enum):
    """ Level Type """
    UNDEFINED = 0
    SCHEDULED = 1
    COMPLETED = 2
    CANCELED = 3
    RESCHEDULED = 4
    FORFEIT = 5


class Base(BaseModel):
    id: UUID4


class BaseCreate(BaseModel):
    pass


class Season(BaseModel):
    id: UUID4
    name: Annotated[str, StringConstraints(max_length=100)]
    start_dt: date
    end_dt: date
    active: bool

    class Config:
        from_attributes = True

class SeasonCreate(BaseCreate):
    name: str
    start_dt: date
    end_dt: date
    active: Optional[bool] = True

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


class MisconductCreate(BaseModel):
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
