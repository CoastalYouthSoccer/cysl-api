from typing import Optional
from pydantic import StringConstraints
from typing_extensions import Annotated
from .base import Base, BaseCreate

class Association(Base):
    name: Annotated[str, StringConstraints(max_length=100)]
    active: bool

    class Config:
        from_attributes = True


class AssociationCreate(BaseCreate):
    name: str
    active: Optional[bool] = True

    class Config:
        from_attributes = True
        