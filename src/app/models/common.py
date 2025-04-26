from enum import Enum
from sqlmodel import SQLModel
from typing import Optional


class GenderEnum(Enum):
    BOYS = 1
    GIRLS = 0


class SQLNameBase(SQLModel):
    name: str
    active: Optional[bool] = True


class SQLBase(SQLModel):
    active: Optional[bool] = True
