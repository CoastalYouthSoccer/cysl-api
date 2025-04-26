import uuid

from typing import Optional
from sqlmodel import Field, Relationship
from .common import SQLNameBase
from .association import Association
from .address import Address


class VenueBase(SQLNameBase):
    address_id: uuid.UUID = Field(default=None, foreign_key="address.id")
    association_id: uuid.UUID = Field(default=None, foreign_key="association.id")


class Venue(VenueBase, table=True):
    __tablename__: str = 'venue'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)
    address: Optional["Address"] = Relationship(back_populates="venues")
    association: Optional["Association"] = Relationship(back_populates="venues")
    sub_venues: Optional["SubVenue"] = Relationship(back_populates="venue")


class VenueCreate(VenueBase):
    pass

class SubVenueBase(SQLNameBase):
    venue_id: uuid.UUID = Field(default=None, foreign_key="venue.id")


class SubVenue(SubVenueBase, table=True):
    __tablename__: str = 'sub_venue'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)
    venue: Venue = Relationship(back_populates="sub_venues")


class SubVenueCreate(SubVenueBase):
    pass
