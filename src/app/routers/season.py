from fastapi import APIRouter, Depends, Security, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.crud import (get_seasons, create_season, deactivate_season,
                      get_season_by_name)
from app.schemas import (Season, SeasonCreate)
from app.dependencies import auth

router = APIRouter()

@router.get("/seasons", response_model=list[Season])
async def read_seasons(db: AsyncSession=Depends(get_session), skip: int=0, limit: int=100):
    return await get_seasons(db, skip=skip, limit=limit)

@router.post("/seasons", response_model=SeasonCreate, status_code=201)
async def new_season(item: SeasonCreate, db: Session=Depends(get_session),
               _: str = Security(auth.verify,
                                 scopes=['write:season'])):
    return await create_season(db, item=item)

@router.delete("/seasons/{id}")
async def delete_season(id: UUID4, db: Session=Depends(get_session),
                  _: str = Security(auth.verify,
                                    scopes=['delete:season'])):
    error = await deactivate_season(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete, {id}!")
    return {"id": id}

@router.get("/seasons/{name}", response_model=Season)
async def get_season_by_name(name: str, db: AsyncSession=Depends(get_session)):
    return await get_season_by_name(db, name=name)
