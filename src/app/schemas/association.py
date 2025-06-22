from typing import Optional
from pydantic import StringConstraints, UUID4
from typing_extensions import Annotated
from .base import Base, BaseCreate


class AssociationCreate(BaseCreate):
    name: Annotated[str, StringConstraints(max_length=100)]
    president: UUID4
    secretary: UUID4
    assignor: UUID4
    registrar: UUID4
    active: Optional[bool] = True

    class Config:
        from_attributes = True


class Association(AssociationCreate):
    id: UUID4
