from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_session

from app.crud import (get_age_groups)
from app.schemas import (AgeGroup)
from app.dependencies import verify_scopes

verify_write_age_groups = verify_scopes(["write:age_groups"])
verify_read_age_groups = verify_scopes(["read:age_groups"])
verify_delete_age_groups = verify_scopes(["delete:age_groups"])

router = APIRouter()

@router.get("/age-groups", response_model=list[AgeGroup])
async def read_age_groups(db: AsyncSession=Depends(get_session), skip: int=0, limit: int=100):
    return await get_age_groups(db, skip=skip, limit=limit)
