from sys import stdout
import logging
import base64

from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security import HTTPBearer, SecurityScopes
from starlette.middleware.cors import CORSMiddleware
from pydantic import UUID4
from typing import Dict

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from app.crud import (get_seasons, create_season, deactivate_season,
                      create_misconduct, get_misconducts, get_associations,
                      deactivate_association, create_association)
from app.schemas import (Season, SeasonCreate, Misconduct, MisconductCreate,
                         Association, AssociationCreate, Venue, VenueGame, GameTimes)
from app.assignr.assignr import Assignr

from app.config import get_settings

from app.helpers.helpers import VerifyToken

config = get_settings()

class SpanFormatter(logging.Formatter):
    def format(self, record):
        trace_id = trace.get_current_span().get_span_context().trace_id
        if trace_id == 0:
            record.trace_id = None
        else:   
            record.trace_id = "{trace:32x}".format(trace=trace_id)
        return super().format(record)

from app.database import get_session

resource = Resource(attributes={
    SERVICE_NAME: config.otel_service_name
})

tracer_provider = TracerProvider(resource=resource)

if config.otel_insecure:
    otlp_exporter = OTLPSpanExporter(
        endpoint=config.otel_exporter_oltp_endpoint,
        insecure="true"
    )
else:    
    auth = base64.b64encode(bytes(f'{config.otel_instance_id}:{config.otel_grafana_token}', 'utf-8')) # bytes
    otlp_exporter = OTLPSpanExporter(
        endpoint=config.otel_exporter_oltp_endpoint,
        headers={
            "Authorization": f"Bearer {auth}"
        }
    )
    
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(span_exporter=otlp_exporter)
)

formatter = SpanFormatter('level=%(levelname)s msg=%(message)s TraceID=%(trace_id)s')
logging.basicConfig(stream=stdout,
                    level=config.log_level)
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()

token_auth_scheme = HTTPBearer()
auth = VerifyToken(config.auth0_domain, config.auth0_algorithms,
                   config.auth0_api_audience, config.auth0_issuer)
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

# venue endpoints
@app.get("/venues", response_model=list[Venue])
def read_venues():
    return assignr.get_venues()

# game endpoints
@app.get("/games", response_model=Dict[str, Dict[str, VenueGame]])
def read_games(start_dt: str, end_dt: str, venue: str | None = None,
    _: str = Security(auth.verify,
                                 scopes=['read:games']
    )):
    return assignr.get_games_venue(start_dt=start_dt, end_dt=end_dt,
                                   venue=venue)

# association endpoints
@app.get("/associations", response_model=list[Association])
async def read_associations(db: AsyncSession=Depends(get_session), skip: int=0, limit: int=100):
    return await get_associations(db, skip=skip, limit=limit)

@app.post("/associations", response_model=AssociationCreate, status_code=201)
async def new_association(item: AssociationCreate, db: Session=Depends(get_session),
               _: str = Security(auth.verify,
                                 scopes=['write:association'])):
    return await create_association(db, item=item)

@app.delete("/associations/{id}")
async def delete_association(id: UUID4, db: Session=Depends(get_session),
                  _: str = Security(auth.verify,
                                    scopes=['delete:association'])):
    error = await deactivate_association(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete Association, {id}!")
    return {"id": id}

# season endpoints
@app.get("/seasons", response_model=list[Season])
async def read_seasons(db: AsyncSession=Depends(get_session), skip: int=0, limit: int=100):
    return await get_seasons(db, skip=skip, limit=limit)

@app.post("/seasons", response_model=SeasonCreate, status_code=201)
async def new_season(item: SeasonCreate, db: Session=Depends(get_session),
               _: str = Security(auth.verify,
                                 scopes=['write:season'])):
    return await create_season(db, item=item)

@app.delete("/seasons/{id}")
async def delete_season(id: UUID4, db: Session=Depends(get_session),
                  _: str = Security(auth.verify,
                                    scopes=['delete:season'])):
    error = await deactivate_season(db, id=id)
    if error:
        raise HTTPException(status_code=400,
                            detail=f"Failed to Delete, {id}!")
    return {"id": id}

@app.post("/misconducts", response_model=Misconduct, status_code=201)
async def new_misconduct(item: MisconductCreate, db: Session=Depends(get_session),
                    _: str = Security(auth.verify,
                    scopes=['write:misconduct'])):
    return await create_misconduct(db, item=item)

@app.get("/misconducts", response_model=list[Misconduct], status_code=200)
async def read_misconducts(db: Session=Depends(get_session),
                    skip: int=0, limit: int=100):
    return await get_misconducts(db, skip=skip, limit=limit)

FastAPIInstrumentor().instrument_app(app)
