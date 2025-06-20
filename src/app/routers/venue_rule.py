from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.crud import (get_venue_rules, create_venue_rule, deactivate_venue_rule,
                      get_venue_rule_by_id, update_venue_rule)
from app.schemas import (SeasonCreate, Season)
from app.dependencies import verify_scopes

verify_write_venue_rules = verify_scopes(["write:venue_rules"])
verify_read_venue_rules = verify_scopes(["read:venue_rules"])
verify_delete_venue_rules = verify_scopes(["delete:venue_rules"])

router = APIRouter()

@router.get("/venue_rules", response_model=list[Season])
async def read_venue_rules(
    db: AsyncSession=Depends(get_session),
    skip: int=0,
    limit: int=100,
    name: Optional[str]=None,
    _: str = Depends(verify_read_venue_rules)):
    return await get_venue_rules(db, skip=skip, limit=limit, name=name)

@router.post("/venue_rule", response_model=Season, status_code=201)
async def new_venue_rule(item: SeasonCreate, db: Session=Depends(get_session),
               _: str = Depends(verify_write_venue_rules)):
    return await create_venue_rule(db, item=item)

@router.patch("/venue_rule", response_model=Season, status_code=201)
async def change_venue_rule(item: Season, db: Session=Depends(get_session),
               _: str = Depends(verify_write_venue_rules)):
    return await update_venue_rule(db, item=item)

@router.delete("/venue_rule/{id}", status_code=204)
async def delete_venue_rule(id: UUID4, db: Session=Depends(get_session),
                  _: str = Depends(verify_delete_venue_rules)):
    return await deactivate_venue_rule(db, id=id)

@router.get("/venue_rule/{id}", response_model=Season)
async def get_venue_rule_id(id: UUID4, db: AsyncSession=Depends(get_session),
                        _: str = Depends(verify_read_venue_rules)):
    return await get_venue_rule_by_id(db, id=id)
