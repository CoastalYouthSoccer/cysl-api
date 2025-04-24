from typing import Optional
from pydantic import StringConstraints, UUID4
from typing_extensions import Annotated
from .base import BaseCreate


class DivisionCreate(BaseCreate):
    name: Annotated[str, StringConstraints(max_length=100)]
    active: Optional[bool] = True

    class Config:
        from_attributes = True


class Division(DivisionCreate):
    id: UUID4
