from typing import Optional
from pydantic import StringConstraints, ConfigDict
from uuid import UUID
from typing_extensions import Annotated
from .base import BaseCreate


class DivisionCreate(BaseCreate):
    name: Annotated[str, StringConstraints(max_length=100)]
    active: Optional[bool] = True

    model_config = ConfigDict(
        from_attributes=True
    )


class Division(DivisionCreate):
    id: UUID
