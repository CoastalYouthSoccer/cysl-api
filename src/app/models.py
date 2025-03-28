from datetime import datetime, date
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


class AssociationBase(SQLModel):
    name: str
    active: bool


class Association(AssociationBase, table=True):
    __tablename__: str = 'association'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class AssociationCreate(AssociationBase):
    pass


class MisconductBase(SQLModel):
    game_dt: datetime
    venue: str
    age_group: str
    gender: str
    home_team: str
    home_team_coach: str
    home_score: int
    away_team: str
    away_team_coach: str
    away_score: int
    reported_by: str
    referee: str
    ar1: Optional[str]
    ar2: Optional[str]
    code: str
    offender_name: str
    coach_player: str
    player_nbr: str
    offender_team: str
    minute: int
    offense: str
    description: str

class Misconduct(MisconductBase, table=True):
    __tablename__: str = 'misconduct'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)

class MisconductCreate(MisconductBase):
    pass


class SeasonBase(SQLModel):
    name: str
    start_dt: date
    end_dt: date
    active: bool


class Season(SeasonBase, table=True):
    __tablename__: str = 'season'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class SeasonCreate(SeasonBase):
    pass


class SubVenueBase(SQLModel):
    name: str
    venue_id: int = Field(default=None, foreign_key="venue.id")
    active: bool


class SubVenue(SubVenueBase, table=True):
    __tablename__: str = 'sub_venue'
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                            primary_key=True)


class SubVenueCreate(SeasonBase):
    pass


class VenueBase(SQLModel):
    name: str
    active: bool
    address_id: int = Field(default=None, foreign_key="address.id")
    association_id: int = Field(default=None, foreign_key="association.id")


class Venue(VenueBase, table=True):
    __tablename__: str = 'venue'
    id: int = Field(default_factory=int,
                            primary_key=True)


class VenueCreate(SeasonBase):
    pass
