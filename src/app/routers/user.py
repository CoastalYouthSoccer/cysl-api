from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from app.database import get_session
from app.crud import (get_users, get_user_by_id,
                      update_user, deactivate_user, get_roles)
from app.schemas import User, Role
from app.dependencies import verify_scopes

verify_write_users = verify_scopes(["write:users"])
verify_read_users = verify_scopes(["read:users"])
verify_delete_users = verify_scopes(["delete:users"])

router = APIRouter()

@router.get("/users", response_model=list[User])
async def read_users(
    page: int=0,
    limit: int=50,
    given_name: Optional[str]=None,
    family_name: Optional[str]=None,
    _: str = Depends(verify_read_users)):
    return await get_users(page=page, limit=limit, given_name=given_name,
                           family_name=family_name)

@router.patch("/user", response_model=User, status_code=201)
async def change_user(user: User, _: str = Depends(verify_write_users)):
    return await update_user(user=user)

@router.delete("/user/{id}", status_code=204)
async def delete_user(id: str, _: str = Depends(verify_delete_users)):
    return await deactivate_user(id=id)

@router.get("/user/{id}", response_model=User)
async def get_user_id(id: str, _: str = Depends(verify_read_users)):
    return await get_user_by_id(id=id)

@router.get("/roles", response_model=list[Role])
async def get_auth0_roles(
    db: AsyncSession=Depends(get_session),
    _: str = Depends(verify_read_users)):
    return await get_roles(db)
