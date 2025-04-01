from fastapi import APIRouter, Depends, Security, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.crud import (get_associations,deactivate_association,
                      create_association)
from app.schemas import (Association, AssociationCreate)
from app.dependencies import auth

router = APIRouter()

@router.get("/associations", response_model=list[Association])
async def read_associations(db: AsyncSession=Depends(get_session), skip: int=0, limit: int=100):
    return await get_associations(db, skip=skip, limit=limit)

@router.post("/associations", response_model=AssociationCreate, status_code=201)
async def new_association(item: AssociationCreate, db: Session=Depends(get_session),
               _: str = Security(auth.verify,
                                 scopes=['write:association'])):
    return await create_association(db, item=item)

@router.delete("/associations/{id}")
async def delete_association(id: UUID4, db: Session=Depends(get_session),
                  _: str = Security(auth.verify,
                                    scopes=['delete:association'])):
    error = await deactivate_association(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete Association, {id}!")
    return {"id": id}