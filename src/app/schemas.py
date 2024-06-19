from enum import Enum
from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, StringConstraints, UUID4
from typing_extensions import Annotated


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


class Venue(BaseModel):
    id: int
    name: str
    city: str | None


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


class Association(BaseModel):
    id: UUID4
    name: Annotated[str, StringConstraints(max_length=100)]
    active: bool

    class Config:
        from_attributes = True


class AssociationCreate(BaseCreate):
    name: str
    active: Optional[bool] = True

    class Config:
        from_attributes = True


class RefereeAssignment(BaseModel):
    accepted: bool
    position: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        from_attributes = True


class Game(BaseModel):
    officials: Optional[list[RefereeAssignment]] = None
    game_date: str
    game_time: str
    home_team: str
    away_team: str
    venue: str
    sub_venue: Optional[str]
    game_type: Optional[str]
    age_group: str
    gender: str
    assignor: Optional[str]

    class Config:
        from_attributes = True
