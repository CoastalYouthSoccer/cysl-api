from typing import Optional
from pydantic import UUID4
from .base import BaseCreate


class AddressCreate(BaseCreate):
    address1: str
    address2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    active: Optional[bool] = True

    class Config:
        from_attributes = True


class Address(AddressCreate):
    id: UUID4
