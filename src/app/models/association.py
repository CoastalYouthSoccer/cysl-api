from datetime import time
import uuid

from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from .common import SQLNameBase


class AssociationBase(SQLNameBase):
    pass


class Association(AssociationBase, table=True):
    __tablename__: str = 'association'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)
    venues: list["Venue"] = Relationship(back_populates='association',
                                         sa_relationship_kwargs={"lazy": "selectin"})


class AssociationCreate(AssociationBase):
    pass


class AssociationGameInfoBase(SQLModel):
    __tablename__: str = 'association_game_info'
    association_id: uuid.UUID = Field(default=None, foreign_key="association.id")
    age_group_id: uuid.UUID = Field(default=None, foreign_key="age_group.id")
    start_time: time
    slot_length: int  # Length of the time to slot between games


class AssociationGameInfo(AssociationGameInfoBase, table=True):
    __tablename__: str = 'association_game_info'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class AssociationGameInfoCreate(AssociationGameInfoBase):
    pass
