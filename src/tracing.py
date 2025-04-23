import base64

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from app.config import get_settings

config = get_settings()

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
