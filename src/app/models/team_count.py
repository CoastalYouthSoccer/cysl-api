import uuid

from sqlmodel import SQLModel, Field
from app.models.common import GenderEnum

class TeamCountBase(SQLModel):
    season_id: uuid.UUID = Field(default=None, foreign_key="season.id",
                                 primary_key=True)
    division_id: uuid.UUID = Field(default=None, foreign_key="division.id",
                                   primary_key=True)
    age_group_id: uuid.UUID = Field(default=None, foreign_key="age_group.id",
                                    primary_key=True)
    gender: int = Field(default=None, primary_key=True)
    association_id: uuid.UUID = Field(default=None, foreign_key="association.id",
                                      primary_key=True)
    team_cnt: int = 0


class TeamCount(TeamCountBase, table=True):
    __tablename__: str = 'team_count'


class TeamCountCreate(TeamCountBase):
    pass