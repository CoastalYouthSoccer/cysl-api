from pydantic import UUID4, ConfigDict
from .base import BaseCreate


class VenueRuleCreate(BaseCreate):
    association_id: str
    age_group_id: str
    gender_boy: bool
    division_id: str
    venue: str
    sub_venue: str

    model_config = ConfigDict(
        from_attributes=True
    )


class VenueRule(VenueRuleCreate):
    id: UUID4

    model_config = ConfigDict(
        from_attributes=True
    )
