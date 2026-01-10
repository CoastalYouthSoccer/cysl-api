from typing import Optional
from uuid import UUID
from .base import BaseCreate
from pydantic import ConfigDict


class AddressCreate(BaseCreate):
    address1: str
    address2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    active: Optional[bool] = True

    model_config = ConfigDict(
        from_attributes=True
    )


class Address(AddressCreate):
    id: UUID
