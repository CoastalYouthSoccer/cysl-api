from sys import stdout
import logging
import base64

from fastapi import FastAPI, Security
from fastapi.security import HTTPBearer
from starlette.middleware.cors import CORSMiddleware
from typing import Dict

from app.schemas import AssignrVenue, VenueGame
from app.assignr.assignr import Assignr
from app.routers import (age_group, association, misconduct, season, game,
                         division, venue, sub_venue, user, person,
                         venue_rule)
from app.config import get_settings
from app.dependencies import auth

config = get_settings()

logging.basicConfig(stream=stdout,
                    level=config.log_level)
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()

token_auth_scheme = HTTPBearer()

assignr = Assignr(config.assignr_client_id, config.assignr_client_secret,
                  config.assignr_client_scope, config.assignr_base_url,
                  config.assignr_auth_url)

app = FastAPI()

origins = config.http_origins.split()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

# Assignr endpoints
@app.get("/assignr-venues", response_model=list[AssignrVenue])
def read_venues():
    return assignr.get_venues()

@app.get("/assignr-games", response_model=Dict[str, Dict[str, VenueGame]])
def read_games(start_dt: str, end_dt: str, venue: str | None = None,
    _: str = Security(auth.verify,
                                 scopes=['read:games']
    )):
    return assignr.get_games_venue(start_dt=start_dt, end_dt=end_dt,
                                   venue=venue)
# game endpoints
app.include_router(game.router)

# association endpoints
app.include_router(association.router)

# division endpoints
app.include_router(division.router)

# season endpoints
app.include_router(season.router)

# age group endpoints
app.include_router(age_group.router)

# misconduct endpoints
app.include_router(misconduct.router)

# venue endpoints
app.include_router(venue.router)

# sub-venue endpoints
app.include_router(sub_venue.router)

# user endpoints
app.include_router(user.router)

# person endpoints
app.include_router(person.router)

# venue-rules endpoints
app.include_router(venue_rule.router)
