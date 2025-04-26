from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.crud import (get_venues,deactivate_venue,
                      create_venue, get_venue_by_id)
from app.schemas import (Venue, VenueCreate)
from app.dependencies import verify_scopes

verify_write_venues = verify_scopes(["write:venues"])
verify_read_venues = verify_scopes(["read:venues"])
verify_delete_venues = verify_scopes(["delete:venues"])

router = APIRouter()

@router.get("/venues", response_model=list[Venue])
async def read_venues(
    db: AsyncSession=Depends(get_session),
    skip: int=0,
    limit: int=100,
    name: Optional[str]=None,
    association: Optional[str]=None,
    association_id: Optional[UUID4]=None,
    _: str = Depends(verify_read_venues)
    ):
    return await get_venues(db, skip=skip, limit=limit, name=name,
                            association=association,
                            association_id=association_id)

@router.post("/venues", response_model=Venue, status_code=201)
async def new_venue(item: VenueCreate, db: Session=Depends(get_session),
               _: str = Depends(verify_write_venues)):
    return await create_venue(db, item=item)

@router.delete("/venue/{id}", status_code=204)
async def delete_venue(id: UUID4, db: Session=Depends(get_session),
                  _: str = Depends(verify_delete_venues)):
    return await deactivate_venue(db, id=id)

@router.get("/venue/{id}", response_model=Venue)
async def get_venue_id(id: UUID4, db: Session=Depends(get_session),
                             _: str = Depends(verify_read_venues)):
    return await get_venue_by_id(db, id)
