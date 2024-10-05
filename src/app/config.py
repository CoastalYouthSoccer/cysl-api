from os import environ
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    auth0_algorithms: str
    database_url: str
    log_level: int = 30
    assignr_client_id: str
    assignr_client_secret: str
    assignr_client_scope: str
    assignr_base_url: str
    assignr_auth_url: str
    http_origins: str
    otel_service_name: str = "cysl-backend"
    otel_instance_id: str = ""
    otel_insecure: bool = False
    otel_exporter_oltp_endpoint: str
    otel_exporter_logs_endpoint: str
    otel_grafana_token: str
    model_config = SettingsConfigDict(env_file=environ.get("ENV_FILE", ".env"),
                                      extra="ignore")


def get_settings():
    return Settings()
