import uuid

from typing import Optional

from sqlmodel import Field, Relationship
from .common import SQLBase


class AddressBase(SQLBase):
    address1: str
    address2: Optional[str] = Field(default=None, nullable=True)
    city: str
    state: str
    zip_code: str


class Address(AddressBase, table=True):
    __tablename__: str = 'address'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)
    venues: list["Venue"] = Relationship(back_populates='address',
                                         sa_relationship_kwargs={"lazy": "selectin"})


class AddressCreate(AddressBase):
    pass
