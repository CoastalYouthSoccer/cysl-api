from pydantic import StringConstraints
from typing_extensions import Annotated
from .base import Base


class AgeGroup(Base):
    name: Annotated[str, StringConstraints(max_length=100)]
    game_length: int

    class Config:
        from_attributes = True
