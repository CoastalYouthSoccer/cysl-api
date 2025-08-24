from datetime import datetime
import uuid

from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from app.models.common import GenderEnum


class GameBase(SQLModel):
    season_id: uuid.UUID = Field(default=None, foreign_key="season.id")
    division_id: uuid.UUID = Field(default=None, foreign_key="division.id")
    age_group_id: uuid.UUID = Field(default=None, foreign_key="age_group.id")
    gender_boy: bool = Field(default=None)
    home_team: str
    away_team: str
    sub_venue_id: Optional[uuid.UUID] = Field(default=None, foreign_key="sub_venue.id")
    game_dt: Optional[datetime] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None

    @property
    def venue_id(self):
        return self.sub_venue.venue.id if self.sub_venue else None

class Game(GameBase, table=True):
    __tablename__: str = 'game'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)
    sub_venue: Optional["SubVenue"] = Relationship(back_populates="games")


class GameCreate(GameBase):
    pass