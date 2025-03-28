from fastapi import APIRouter, Depends, Security, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_session

from app.crud import (get_age_groups)
from app.schemas import (AgeGroup)


router = APIRouter()

@router.get("/age-groups", response_model=list[AgeGroup])
async def read_age_groups(db: AsyncSession=Depends(get_session), skip: int=0, limit: int=100):
    return await get_age_groups(db, skip=skip, limit=limit)
