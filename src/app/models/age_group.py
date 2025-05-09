import uuid

from sqlmodel import Field
from .common import SQLNameBase

class AgeGroupBase(SQLNameBase):
    game_length:int


class AgeGroup(AgeGroupBase, table=True):
    __tablename__: str = 'age_group'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class AgeGroupCreate(AgeGroupBase):
    pass
