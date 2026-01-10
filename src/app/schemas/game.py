from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

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

    model_config = ConfigDict(
        from_attributes=True
    )
