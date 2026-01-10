from pydantic import StringConstraints, ConfigDict
from typing_extensions import Annotated
from .base import Base


class AgeGroup(Base):
    name: Annotated[str, StringConstraints(max_length=100)]
    game_length: int

    model_config = ConfigDict(
        from_attributes=True
    )

