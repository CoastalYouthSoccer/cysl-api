from sys import stdout
import logging

from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security import HTTPBearer, SecurityScopes
from pydantic import UUID4

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session

from app.crud import (get_seasons, create_season, deactivate_season,
                      create_misconduct, get_misconducts)
from app.schemas import (Season, SeasonCreate, Misconduct, MisconductCreate)

from app.config import get_settings

from app.utils import VerifyToken

config = get_settings()

logging.basicConfig(stream=stdout,
                    level=config.log_level)
logger = logging.getLogger(__name__)

from app.database import get_session

token_auth_scheme = HTTPBearer()
auth = VerifyToken() 

app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

# season endpoints
@app.get("/seasons", response_model=list[Season])
async def read_seasons(db: AsyncSession=Depends(get_session), skip: int=0, limit: int=100):
    return await get_seasons(db, skip=skip, limit=limit)

@app.post("/season", response_model=SeasonCreate, status_code=201)
async def new_season(item: SeasonCreate, db: Session=Depends(get_session),
               _: str = Security(auth.verify,
                                 scopes=['write:season'])):
    return await create_season(db, item=item)

@app.delete("/season/{id}")
async def delete_season(id: UUID4, db: Session=Depends(get_session),
                  _: str = Security(auth.verify,
                                    scopes=['delete:season'])):
    error = await deactivate_season(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete, {id}!")
    return {"id": id}

@app.post("/misconduct", response_model=Misconduct, status_code=201)
async def new_misconduct(item: MisconductCreate, db: Session=Depends(get_session),
                    _: str = Security(auth.verify,
                    scopes=['write:misconduct'])):
    return await create_misconduct(db, item=item)

@app.get("/misconducts", response_model=list[Misconduct], status_code=200)
async def read_misconducts(db: Session=Depends(get_session),
                    skip: int=0, limit: int=100):
    return await get_misconducts(db, skip=skip, limit=limit)
