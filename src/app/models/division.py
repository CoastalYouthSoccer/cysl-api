import uuid

from sqlmodel import SQLModel, Field


class DivisionBase(SQLModel):
    name: str
    active: bool


class Division(DivisionBase, table=True):
    __tablename__: str = 'division'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class DivisionCreate(DivisionBase):
    pass