import logging
from fastapi import APIRouter, Depends, Security, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.crud import (get_seasons, create_season, deactivate_season,
                      get_season_by_name, get_season_by_id)
from app.schemas import (SeasonCreate, Season)
from app.dependencies import verify_scopes

logger = logging.getLogger(__name__)

verify_write_seasons = verify_scopes(["write:seasons"])

router = APIRouter()

@router.get("/seasons", response_model=list[Season])
async def read_seasons(db: AsyncSession=Depends(get_session), skip: int=0,
                       limit: int=100, name: str=None):
    return await get_seasons(db, skip=skip, limit=limit, name=name)

@router.post("/seasons", response_model=Season, status_code=201)
async def new_season(item: SeasonCreate, db: Session=Depends(get_session),
               _: str = Depends(verify_write_seasons)):
    return await create_season(db, item=item)

@router.delete("/season/{id}")
async def delete_season(id: UUID4, db: Session=Depends(get_session),
                  _: str = Depends(verify_scopes(["delete:seasons"]))):
    error = await deactivate_season(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete, {id}!")
    return {"id": id}

#@router.get("/seasons/{name}", response_model=Season)
#async def get_season_name(name: str, db: AsyncSession=Depends(get_session)):
#    return await get_season_by_name(db, name=name)

@router.get("/season/{id}", response_model=Season)
async def get_season_id(id: UUID4, db: AsyncSession=Depends(get_session)):
    return await get_season_by_id(db, id=id)
