from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel
from .venue_sub_venue import Venue, SubVenue

class GameStatus(Enum):
    """ Level Type """
    UNDEFINED = 0
    SCHEDULED = 1
    COMPLETED = 2
    CANCELED = 3
    RESCHEDULED = 4
    FORFEIT = 5


class Game(BaseModel):
    id: UUID4
    season_id: UUID4
    division_id: UUID4
    age_group_id: UUID4
    gender_boy: bool
    home_team: str
    away_team: str
    venue_id: Optional[UUID4] = None
    sub_venue_id: Optional[UUID4] = None
    game_dt: Optional[datetime] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None

    class Config:
        from_attributes = True
