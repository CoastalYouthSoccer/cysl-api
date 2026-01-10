from pydantic import UUID4, EmailStr, ConfigDict
from .base import BaseCreate


class PersonCreate(BaseCreate):
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


class Person(PersonCreate):
    id: UUID4

    model_config = ConfigDict(
        from_attributes=True
    )
