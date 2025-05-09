import uuid

from sqlmodel import Field
from .common import SQLNameBase


class DivisionBase(SQLNameBase):
    pass


class Division(DivisionBase, table=True):
    __tablename__: str = 'division'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class DivisionCreate(DivisionBase):
    pass