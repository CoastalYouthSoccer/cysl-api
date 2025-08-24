import uuid
from typing import Optional

from sqlmodel import SQLModel, Field


class SubVenueBase(SQLModel):
    name: str
    venue_id: uuid.UUID = Field(default=None, foreign_key="venue.id")
    active: bool


class SubVenue(SubVenueBase, table=True):
    __tablename__: str = 'sub_venue'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class SubVenueCreate(SubVenueBase):
    pass
