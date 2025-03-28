from fastapi import APIRouter, Depends, Security, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.dependencies import auth

from app.crud import (create_misconduct, get_misconducts)
from app.schemas import (Misconduct, MisconductCreate)

router = APIRouter()

@router.post("/misconducts", response_model=Misconduct, status_code=201)
async def new_misconduct(item: MisconductCreate, db: Session=Depends(get_session),
                    _: str = Security(auth.verify,
                    scopes=['write:misconduct'])):
    return await create_misconduct(db, item=item)

@router.get("/misconducts", response_model=list[Misconduct], status_code=200)
async def read_misconducts(db: Session=Depends(get_session),
                    skip: int=0, limit: int=100):
    return await get_misconducts(db, skip=skip, limit=limit)
