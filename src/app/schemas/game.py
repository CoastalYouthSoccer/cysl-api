from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel
from .base import Base, BaseCreate

class GameStatus(Enum):
    """ Level Type """
    UNDEFINED = 0
    SCHEDULED = 1
    COMPLETED = 2
    CANCELED = 3
    RESCHEDULED = 4
    FORFEIT = 5


class Gender(Enum):
    BOYS = 1
    GIRLS = 0


class Game(BaseModel):
    season_id: UUID4
    division_id: UUID4
    age_group_id: UUID4
    gender: Gender
    home_team: str
    away_team: str
    sub_venue_id: Optional[UUID4] = None
    game_dt: Optional[datetime] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None

    class Config:
        from_attributes = True

