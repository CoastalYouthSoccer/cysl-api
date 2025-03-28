from datetime import date
from typing import Optional
from pydantic import StringConstraints
from typing_extensions import Annotated
from .base import Base, BaseCreate


class Season(Base):
    name: Annotated[str, StringConstraints(max_length=100)]
    start_dt: date
    season_length: int
    holiday_dates: Optional[str]
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
