from sys import stdout
import logging
import base64

from fastapi import FastAPI, Security, HTTPException
from fastapi.security import HTTPBearer, SecurityScopes
from starlette.middleware.cors import CORSMiddleware
from typing import Dict

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from app.schemas import (Game, AgeGroup, Association, Venue, Season, Misconduct)
from app.assignr.assignr import Assignr
from app.routers import (age_group, association, misconduct, season, game)
from app.config import get_settings
from app.dependencies import auth

config = get_settings()

class SpanFormatter(logging.Formatter):
    def format(self, record):
        trace_id = trace.get_current_span().get_span_context().trace_id
        if trace_id == 0:
            record.trace_id = None
        else:   
            record.trace_id = "{trace:32x}".format(trace=trace_id)
        return super().format(record)

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
    oltp_auth = base64.b64encode(bytes(f'{config.otel_instance_id}:{config.otel_grafana_token}', 'utf-8')) # bytes
    otlp_exporter = OTLPSpanExporter(
        endpoint=config.otel_exporter_oltp_endpoint,
        headers={
            "Authorization": f"Bearer {oltp_auth}"
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
app.include_router(game.router)

# association endpoints
app.include_router(association.router)

# season endpoints
app.include_router(season.router)

# age group endpoints
app.include_router(age_group.router)

# misconduct endpoints
app.include_router(misconduct.router)

#FastAPIInstrumentor().instrument_app(app)
