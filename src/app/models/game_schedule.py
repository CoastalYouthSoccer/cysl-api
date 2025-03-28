from datetime import datetime
import uuid

from typing import Optional

from sqlmodel import SQLModel, Field


class GameScheduleBase(SQLModel):
    season_id: uuid.UUID = Field(default=None, foreign_key="season.id")
    division_id: uuid.UUID = Field(default=None, foreign_key="division.id")
    age_group_id: uuid.UUID = Field(default=None, foreign_key="age_group.id")
    home_team: str
    away_team: str
    sub_venue_id: Optional[uuid.UUID] = Field(default=None, foreign_key="sub_venue.id")
    game_dt: Optional[datetime] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None


class GameSchedule(GameScheduleBase, table=True):
    __tablename__: str = 'game_schedule'
    id: uuid.UUID = Field(default_factory=int,
                            primary_key=True)


class GameScheduleCreate(GameScheduleBase):
    pass