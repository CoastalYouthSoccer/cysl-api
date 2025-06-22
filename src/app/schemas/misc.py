from typing import Optional, Dict
from pydantic import BaseModel


class GameReport(BaseModel):
    author: Optional[str] = None
    misconducts: Optional[bool] = None
    ejections: Optional[bool] = None
    no_show: Optional[bool] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None

    class Config:
        from_attributes = True


class RefereeAssignment(BaseModel):
    accepted: bool
    position: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        from_attributes = True


class VenueGame(BaseModel):
    officials: Optional[list[RefereeAssignment]] = None
    home_team: str
    away_team: str
    age_group: str
    gender: str
    report: Optional[GameReport] = None

    class Config:
        from_attributes = True


class GameTimes(BaseModel):
    games: Dict[str, VenueGame]


class VenueSchedule(BaseModel):
    fields: Dict[str, GameTimes]
