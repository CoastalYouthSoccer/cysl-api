from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.crud import (get_divisions, deactivate_division,
                      create_division, get_division_by_id)
from app.schemas import (Division, DivisionCreate)
from app.dependencies import verify_scopes

verify_write_divisions = verify_scopes(["write:divisions"])
verify_read_divisions = verify_scopes(["read:divisions"])
verify_delete_divisions = verify_scopes(["delete:divisions"])

router = APIRouter()

@router.get("/divisions", response_model=list[Division])
async def read_divisions(
    db: AsyncSession=Depends(get_session),
    skip: int=0,
    limit: int=100,
    name: Optional[str]=None,
    _: str = Depends(verify_read_divisions)
    ):
    return await get_divisions(db, skip=skip, limit=limit, name=name)

@router.post("/divisions", response_model=Division, status_code=201)
async def new_division(item: DivisionCreate, db: Session=Depends(get_session),
               _: str = Depends(verify_write_divisions)):
    return await create_division(db, item=item)

@router.delete("/division/{id}", status_code=204)
async def delete_division(id: UUID4, db: Session=Depends(get_session),
                  _: str = Depends(verify_delete_divisions)):
    return await deactivate_division(db, id=id)

@router.get("/division/{id}", response_model=Division)
async def get_division_id(id: UUID4, db: Session=Depends(get_session),
                              _: str = Depends(verify_read_divisions)):
    return await get_division_by_id(db, id)
