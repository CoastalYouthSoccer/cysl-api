from os import environ
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    management_auth0_domain: str
    management_auth0_client_id: str
    management_auth0_client_secret: str
    auth0_issuer: str
    auth0_algorithms: str = "RS256"
    database_url: str
    celery_database_url: str
    log_level: int = 30
    assignr_client_id: str
    assignr_client_secret: str
    assignr_client_scope: str = "read write"
    assignr_base_url: str = "https://api.assignr.com/api/v2/"
    assignr_auth_url: str = "https://app.assignr.com/oauth/token"
    http_origins: str = "*"
    otel_service_name: str = "cysl-backend"
    otel_instance_id: str = ""
    otel_insecure: bool = False
    otel_exporter_oltp_endpoint: str
    otel_grafana_token: str
    db_encryption_key: str
    hmac_secret: str
    model_config = SettingsConfigDict(env_file=environ.get("ENV_FILE", ".env"),
                                      extra="ignore")


def get_settings():
    return Settings()
