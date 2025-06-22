import uuid

from sqlmodel import Field
from .common import SQLBase


class VenueRuleBase(SQLBase):
    association_id: uuid.UUID = Field(foreign_key="association.id")
    age_group_id: uuid.UUID = Field(foreign_key="age_group.id")
    gender_boy: bool = Field(default=None)
    division_id: uuid.UUID = Field(default=None, foreign_key="division.id")
    venue: str
    sub_venue: str


class VenueRule(VenueRuleBase, table=True):
    __tablename__: str = 'venue_rule'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class VenueRuleCreate(VenueRuleBase):
    pass