from sqlmodel import SQLModel, Field

# Table corresponds to the roles in Auth0. Table exists to
# reduce the number of calls to Auth0 Management API.
class Auth0Role(SQLModel, table=True):
    __tablename__: str = 'auth0_role'
    id: str = Field(primary_key=True)
    name: str
    description: str
