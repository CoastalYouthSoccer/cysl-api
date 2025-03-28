from pydantic import BaseModel, UUID4


class Base(BaseModel):
    id: UUID4


class BaseCreate(BaseModel):
    pass
