from datetime import date
from pydantic import StringConstraints
from typing_extensions import Annotated
from uuid import UUID
from .base import BaseCreate


class SeasonCreate(BaseCreate):
    name: Annotated[str, StringConstraints(max_length=100)]
    start_dt: date
    season_length: int
    holiday_dates: str | None = None

    class Config:
        from_attributes = True


class Season(SeasonCreate):
    id: UUID

    class Config:
        from_attributes = True
