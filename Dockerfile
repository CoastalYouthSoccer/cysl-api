FROM python:3.12.7-slim AS container-image

RUN apt-get update && apt-get install --no-install-recommends -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

FROM container-image

RUN useradd -u 5000 app-user
USER app-user

COPY ./src .

RUN pip install -r requirements.txt

ENV OTEL_METRIC_EXPORT_INTERVAL="5000"
ENV OTEL_RESOURCE_ATTRIBUTES=""

ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=false
ENV OTEL_LOGS_EXPORTER=otlp

ENTRYPOINT ["opentelemetry-instrument", "uvicorn" , "main:app", "--port", "9000", \
            "--env-file", "/opt/cysl/backend/.env", "--reload"]
