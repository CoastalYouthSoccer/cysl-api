from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
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
    id: UUID
    season_id: UUID
    division_id: UUID
    age_group_id: UUID
    gender_boy: bool
    home_team: str
    away_team: str
    venue_id: Optional[UUID] = Field(default=None)
    sub_venue_id: Optional[UUID] = Field(default=None)
    game_dt: Optional[datetime] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None

    class Config:
        from_attributes = True
