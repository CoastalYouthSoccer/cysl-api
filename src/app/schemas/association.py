from typing import Optional
from pydantic import StringConstraints, Field, ConfigDict
from typing_extensions import Annotated
from uuid import UUID
from .base import BaseCreate


class AssociationCreate(BaseCreate):
    name: Annotated[str, StringConstraints(max_length=100)]
    president: Optional[UUID] = Field(default=None)
    secretary: Optional[UUID] = Field(default=None)
    assignor: Optional[UUID] = Field(default=None)
    registrar: Optional[UUID] = Field(default=None)
    active: Optional[bool] = True

    model_config = ConfigDict(
        from_attributes=True
    )


class Association(AssociationCreate):
    id: UUID
