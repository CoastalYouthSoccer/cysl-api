import uuid

from sqlmodel import SQLModel, Field

class AgeGroupBase(SQLModel):
    name: str
    game_length:int


class AgeGroup(AgeGroupBase, table=True):
    __tablename__: str = 'age_group'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class AgeGroupCreate(AgeGroupBase):
    pass
