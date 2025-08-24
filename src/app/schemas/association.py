from typing import Optional
from pydantic import StringConstraints, UUID4
from typing_extensions import Annotated
from .base import Base, BaseCreate


class AssociationCreate(BaseCreate):
    name: Annotated[str, StringConstraints(max_length=100)]
    president: Optional[UUID4]
    secretary: Optional[UUID4]
    assignor: Optional[UUID4]
    registrar: Optional[UUID4]
    active: Optional[bool] = True

    class Config:
        from_attributes = True


class Association(AssociationCreate):
    id: UUID4
