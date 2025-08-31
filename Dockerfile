FROM python:3.12.7-slim AS container-image

RUN apt-get update && apt-get install --no-install-recommends -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM container-image

RUN mkdir /app && useradd -m -u 1000 fastapi

WORKDIR /app

COPY ./src/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src .

ENV OTEL_METRIC_EXPORT_INTERVAL="5000"
ENV OTEL_RESOURCE_ATTRIBUTES=""

ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=false
ENV OTEL_LOGS_EXPORTER=otlp

RUN chown -R fastapi /app 
USER fastapi

ENTRYPOINT ["uvicorn" , "main:app", "--host", "0.0.0.0", "--port", "8000"]
