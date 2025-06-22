from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.crud import (get_persons, create_person, deactivate_person,
                      get_person_by_id, update_person)
from app.schemas import (SeasonCreate, Season)
from app.dependencies import verify_scopes

verify_write_persons = verify_scopes(["write:persons"])
verify_read_persons = verify_scopes(["read:persons"])
verify_delete_persons = verify_scopes(["delete:persons"])

router = APIRouter()

@router.get("/persons", response_model=list[Season])
async def read_persons(
    db: AsyncSession=Depends(get_session),
    skip: int=0,
    limit: int=100,
    name: Optional[str]=None,
    _: str = Depends(verify_read_persons)):
    return await get_persons(db, skip=skip, limit=limit, name=name)

@router.post("/person", response_model=Season, status_code=201)
async def new_person(item: SeasonCreate, db: Session=Depends(get_session),
               _: str = Depends(verify_write_persons)):
    return await create_person(db, item=item)

@router.patch("/person", response_model=Season, status_code=201)
async def change_person(item: Season, db: Session=Depends(get_session),
               _: str = Depends(verify_write_persons)):
    return await update_person(db, item=item)

@router.delete("/person/{id}", status_code=204)
async def delete_person(id: UUID4, db: Session=Depends(get_session),
                  _: str = Depends(verify_delete_persons)):
    return await deactivate_person(db, id=id)

@router.get("/person/{id}", response_model=Season)
async def get_person_id(id: UUID4, db: AsyncSession=Depends(get_session),
                        _: str = Depends(verify_read_persons)):
    return await get_person_by_id(db, id=id)
