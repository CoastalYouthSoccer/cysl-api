from pydantic import UUID4, EmailStr
from .base import BaseCreate


class PersonCreate(BaseCreate):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class Person(PersonCreate):
    id: UUID4

    class Config:
        from_attributes = True
