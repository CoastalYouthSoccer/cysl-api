from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.crud import (get_associations,deactivate_association,
                      create_association, get_association)
from app.schemas import (Association, AssociationCreate)
from app.dependencies import verify_scopes

verify_write_associations = verify_scopes(["write:associations"])
verify_read_associations = verify_scopes(["read:associations"])
verify_delete_associations = verify_scopes(["delete:associations"])

router = APIRouter()

@router.get("/associations", response_model=list[Association])
async def read_associations(
    db: AsyncSession=Depends(get_session),
    skip: int=0,
    limit: int=100,
    name: Optional[str]=None,
    _: str = Depends(verify_read_associations)
    ):
    return await get_associations(db, skip=skip, limit=limit, name=name)

@router.post("/associations", response_model=AssociationCreate, status_code=201)
async def new_association(item: AssociationCreate, db: Session=Depends(get_session),
               _: str = Depends(verify_write_associations)):
    return await create_association(db, item=item)

@router.delete("/association/{id}", status_code=204)
async def delete_association(id: UUID4, db: Session=Depends(get_session),
                  _: str = Depends(verify_delete_associations)):
    return await deactivate_association(db, id=id)

@router.get("/association/{id}", response_model=Association)
async def get_association_id(id: UUID4, db: Session=Depends(get_session)):
    return await get_association(db, id)