from typing import Optional

from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Base(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")


class BaseCreate(BaseModel):
    active: Optional[bool] = Field(default=True, description="Whether the record is active")
