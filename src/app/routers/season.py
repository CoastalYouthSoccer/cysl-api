from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.crud import (get_seasons, create_season, deactivate_season,
                      get_season_by_id, update_season)
from app.schemas import (SeasonCreate, Season)
from app.dependencies import verify_scopes

verify_write_seasons = verify_scopes(["write:seasons"])
verify_read_seasons = verify_scopes(["read:seasons"])
verify_delete_seasons = verify_scopes(["delete:seasons"])

router = APIRouter()

@router.get("/seasons", response_model=list[Season])
async def read_seasons(
    db: AsyncSession=Depends(get_session),
    skip: int=0,
    limit: int=100,
    name: Optional[str]=None,
    _: str = Depends(verify_read_seasons)):
    return await get_seasons(db, skip=skip, limit=limit, name=name)

@router.post("/season", response_model=Season, status_code=201)
async def new_season(item: SeasonCreate, db: Session=Depends(get_session),
               _: str = Depends(verify_write_seasons)):
    return await create_season(db, item=item)

@router.patch("/season", response_model=Season, status_code=201)
async def change_season(item: Season, db: Session=Depends(get_session),
               _: str = Depends(verify_write_seasons)):
    return await update_season(db, item=item)

@router.delete("/season/{id}", status_code=204)
async def delete_season(id: UUID4, db: Session=Depends(get_session),
                  _: str = Depends(verify_delete_seasons)):
    return await deactivate_season(db, id=id)

@router.get("/season/{id}", response_model=Season)
async def get_season_id(id: UUID4, db: AsyncSession=Depends(get_session),
                        _: str = Depends(verify_read_seasons)):
    return await get_season_by_id(db, id=id)
