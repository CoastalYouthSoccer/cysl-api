from datetime import date
from typing import Optional
from pydantic import StringConstraints, UUID4
from typing_extensions import Annotated
from .base import BaseCreate


class SeasonCreate(BaseCreate):
    name: Annotated[str, StringConstraints(max_length=100)]
    start_dt: date
    season_length: int
    holiday_dates: str | None = None

    class Config:
        from_attributes = True


class Season(SeasonCreate):
    id: UUID4

    class Config:
        from_attributes = True
