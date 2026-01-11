import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from app.schemas import (User, Role)
from app.models import Auth0Role
from auth0.authentication import GetToken
from auth0.management import Auth0
from app.config import get_settings

logger = logging.getLogger(__name__)

config = get_settings()

def get_auth0():
    get_token = GetToken(
        config.management_auth0_domain, config.management_auth0_client_id,
        config.management_auth0_client_secret
    )
    token = get_token.client_credentials(
        f"https://{config.management_auth0_domain}/api/v2/"
    )['access_token']
    return Auth0(config.management_auth0_domain, token)

def get_roles_per_user(users):
    auth0 = get_auth0()
    for user in users:
        roles = auth0.users.list_roles(user['user_id'])
        user['roles'] = roles
    parsed_users = [parse_auth0_user(u) for u in users]
    return parsed_users

def parse_auth0_user(auth0_data: dict) -> User:
    associations = auth0_data.get("user_metadata", {}).get("associations", [])
    if isinstance(associations, str):
        associations = [associations]
    elif not isinstance(associations, list):
        associations = []

    roles_raw = auth0_data.get("roles", [])
    roles = []
    for r in roles_raw['roles']:
        roles.append(Role(**r))

    return User(
        user_id=auth0_data["user_id"],
        email=auth0_data["email"],
        email_verified=auth0_data["email_verified"],
        user_name=auth0_data["nickname"],
        created_dt=auth0_data["created_at"],
        updated_dt=auth0_data["updated_at"],
        user_metadata=auth0_data.get("user_metadata", {}),
        name=auth0_data["name"],
        last_login=auth0_data["last_login"],
        given_name=auth0_data.get("given_name", ""),
        family_name=auth0_data.get("family_name", ""),
        roles=roles,
        associations=associations,
    )

async def get_users(page: int=0, limit: int=50, given_name: str=None,
                    family_name: str=None):
    query = None
    auth0 = get_auth0()
    query = ' '.join(
        part for part in [
            f'given_name:{given_name}' if given_name else '',
            f'family_name:{family_name}' if family_name else ''
        ] if part
    )
    if query:
        users = auth0.users.list(q=query,per_page=limit, page=page)["users"]
    else:
        users = auth0.users.list()["users"]

    return get_roles_per_user(users)

async def get_user_by_id(id: str):
    auth0 = get_auth0()
    users = [auth0.users.get(id)]
    return get_roles_per_user(users)[0]

async def update_user(user: User):
    auth0 = get_auth0()

    update_user = {
        "user_metadata": {
            "associations": user.associations
        }
    }

    _ = auth0.users.update(user.user_id, update_user)

    roles = auth0.users.list_roles(user.user_id)
    role_ids = [role['id'] for role in roles['roles']]
    if role_ids:
        _ = auth0.users.remove_roles(user.user_id, role_ids)
    role_ids = [role.id for role in user.roles]
    if role_ids:
        _ = auth0.users.add_roles(user.user_id, role_ids)
    return await get_user_by_id(user.user_id)

async def deactivate_user(id: str):
    auth0 = get_auth0()

    update_user = {
        "user_metadata": {}
    }

    _ = auth0.users.update(id, update_user)

    roles = auth0.users.list_roles(id)
    role_ids = [role['id'] for role in roles['roles']]
    if role_ids:
        _ = auth0.users.remove_roles(id, role_ids)

async def get_roles(session: AsyncSession):
    result = await session.execute(select(Auth0Role))
    return result.scalars().all()
