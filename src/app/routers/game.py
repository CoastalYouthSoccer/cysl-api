from fastapi import APIRouter, Depends, Security, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database import get_session
from app.dependencies import auth

from app.crud import (get_games, create_game, delete_game)
from app.schemas import (Game, GameCreate)


router = APIRouter()

@router.get("/games", response_model=list[Game])
async def read_games(db: AsyncSession=Depends(get_session), skip: int=0, limit: int=100):
#                                      _: str = Security(auth.verify,
#                                 scopes=['read:game'])):
    return await get_games(db, skip=skip, limit=limit)

@router.post("/games", response_model=GameCreate, status_code=201)
async def new_game(item: GameCreate, db: Session=Depends(get_session),
               _: str = Security(auth.verify,
                                 scopes=['write:game'])):
    return await create_game(db, item=item)

@router.post("/games/{id}")
async def update_game(id: UUID4, item: Game, db: Session=Depends(get_session),
               _: str = Security(auth.verify,
                                 scopes=['write:game'])):
    return await update_game(db, id=id, item=item)

@router.delete("/games/{id}")
async def delete_game(id: UUID4, db: Session=Depends(get_session),
                  _: str = Security(auth.verify,
                                    scopes=['delete:game'])):
    error = await delete_game(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete, {id}!")
    return {"id": id}
