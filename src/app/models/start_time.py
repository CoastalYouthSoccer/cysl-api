from datetime import time
import uuid

from typing import Optional

from sqlmodel import SQLModel, Field


class StartTime(SQLModel, table=True):
    __tablename__: str = 'start_time'
    association_id: uuid.UUID = Field(default=None, foreign_key="association.id",
                                 primary_key=True)
    age_group_id: uuid.UUID = Field(default=None, foreign_key="age_group.id",
                                    primary_key=True)
    start_time: time
    slack_time: int
