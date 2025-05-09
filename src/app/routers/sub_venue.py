from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.crud import (get_sub_venues, deactivate_sub_venue,
                      create_sub_venue, get_sub_venue_by_id,
                      update_sub_venue)
from app.schemas import (SubVenue, SubVenueCreate, SubVenueUpdate)
from app.dependencies import verify_scopes

verify_write_venues = verify_scopes(["write:venues"])
verify_read_venues = verify_scopes(["read:venues"])
verify_delete_venues = verify_scopes(["delete:venues"])

router = APIRouter()

@router.get("/sub-venues", response_model=list[SubVenue])
async def read_sub_venues(
    db: AsyncSession=Depends(get_session),
    skip: int=0,
    limit: int=100,
    name: Optional[str]=None,
    venue_id: Optional[UUID4]=None,
    _: str = Depends(verify_read_venues)
    ):
    return await get_sub_venues(db, skip=skip, limit=limit, name=name,
                                venue_id=venue_id)

@router.post("/sub-venue", response_model=SubVenue, status_code=201)
async def new_sub_venue(item: SubVenueCreate, db: Session=Depends(get_session),
               _: str = Depends(verify_write_venues)):
    return await create_sub_venue(db, item=item)

@router.patch("/sub-venue", response_model=SubVenue, status_code=201)
async def change_sub_venue(item: SubVenueUpdate, db: Session=Depends(get_session),
               _: str = Depends(verify_write_venues)):
    return await update_sub_venue(db, item=item)

@router.delete("/sub-venue/{id}", status_code=204)
async def delete_sub_venue(id: UUID4, db: Session=Depends(get_session),
                  _: str = Depends(verify_delete_venues)):
    return await deactivate_sub_venue(db, id=id)

@router.get("/sub-venue/{id}", response_model=SubVenue)
async def get_sub_venue_id(id: UUID4, db: Session=Depends(get_session),
                             _: str = Depends(verify_read_venues)):
    return await get_sub_venue_by_id(db, id)
