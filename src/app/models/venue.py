import uuid

from sqlmodel import SQLModel, Field
from .address import Address  #noqa


class VenueBase(SQLModel):
    name: str
    active: bool
    address_id: uuid.UUID = Field(default=None, foreign_key="address.id")
    association_id: uuid.UUID = Field(default=None, foreign_key="association.id")


class Venue(VenueBase, table=True):
    __tablename__: str = 'venue'
    id: uuid.UUID = Field(default_factory=int,
                            primary_key=True)


class VenueCreate(VenueBase):
    pass
