from datetime import date
import uuid

from typing import Optional

from sqlmodel import SQLModel, Field


class SeasonBase(SQLModel):
    name: str
    start_dt: date
    season_length: int  # Length of the season in weeks
    holiday_dates: Optional[str] = None
    active: Optional[bool] = True


class Season(SeasonBase, table=True):
    __tablename__: str = 'season'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class SeasonCreate(SeasonBase):
    pass


class SeasonRead(SeasonBase):
    id: uuid.UUID
