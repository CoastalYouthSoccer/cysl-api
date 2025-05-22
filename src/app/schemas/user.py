from typing import List
from pydantic import BaseModel

class Role(BaseModel):
    id: str
    name: str
    description: str


class User(BaseModel):
    user_id: str
    email: str
    email_verified: bool
    user_name: str
    created_dt: str
    updated_dt: str
    user_metadata: dict
    name: str
    last_login: str
    given_name: str
    family_name: str
    roles: List[Role] = []
    associations: List[str] = []
