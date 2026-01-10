from pydantic import StringConstraints, UUID4, ConfigDict
from typing_extensions import Annotated
from .base import BaseCreate, Base
from .address import Address
from .association import Association


class VenueCreate(BaseCreate):
    name: Annotated[str, StringConstraints(max_length=100)]
    address: Address
    association: Association

    model_config = ConfigDict(
        from_attributes=True
    )


class Venue(VenueCreate):
    id: UUID4

    model_config = ConfigDict(
        from_attributes=True
    )


class SubVenueCreate(BaseCreate):
    name: Annotated[str, StringConstraints(max_length=100)]
    venue_id: UUID4

    model_config = ConfigDict(
        from_attributes=True
    )


class SubVenueUpdate(SubVenueCreate):
    id: UUID4

    model_config = ConfigDict(
        from_attributes=True
    )


class SubVenue(BaseCreate):
    id: UUID4
    name: Annotated[str, StringConstraints(max_length=100)]
    venue: Venue

    model_config = ConfigDict(
        from_attributes=True
    )


class AssignrVenue(Base):
    id: int
    name: str
    city: str | None
