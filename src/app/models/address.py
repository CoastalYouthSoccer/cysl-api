import uuid

from typing import Optional

from sqlmodel import SQLModel, Field


class AddressBase(SQLModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    zip_code: str


class Address(AddressBase, table=True):
    __tablename__: str = 'address'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class AddressCreate(AddressBase):
    pass
