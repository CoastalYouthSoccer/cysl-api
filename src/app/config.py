from os import environ
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth0_domain: str = Field(..., env="AUTH0_DOMAIN")
    auth0_api_audience: str = Field(..., env="AUTH0_API_AUDIENCE")
    auth0_issuer: str = Field(..., env="AUTH0_ISSUER")
    management_auth0_domain: str = Field(..., env="MANAGEMENT_AUTH0_DOMAIN")
    management_auth0_client_id: str = Field(..., env="MANAGEMENT_AUTH0_CLIENT_ID")
    management_auth0_client_secret: str = Field(..., env="MANAGEMENT_AUTH0_CLIENT_SECRET")
    auth0_algorithms: str = "RS256"
    database_url: str = Field(..., env="DATABASE_URL")
    celery_database_url: str = Field(..., env="CELERY_DATABASE_URL")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    assignr_client_id: str = Field(..., env="ASSIGNR_CLIENT_ID")
    assignr_client_secret: str = Field(..., env="ASSIGNR_CLIENT_SECRET")
    assignr_client_scope: str = "read write"
    assignr_base_url: str = "https://api.assignr.com/api/v2/"
    assignr_auth_url: str = "https://app.assignr.com/oauth/token"
    http_origins: str = "*"
    otel_service_name: str = "cysl-backend"
    otel_instance_id: str = ""
    otel_insecure: bool = False
    otel_exporter_oltp_endpoint: str = Field(..., env="OTEL_EXPORTER_OLTP_ENDPOINT")
    otel_grafana_token: str = Field(..., env="OTEL_GRAFANA_TOKEN")
    db_encryption_key: str = Field(..., env="DB_ENCRYPTION_KEY")
    hmac_secret: str = Field(..., env="HMAC_SECRET")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(
                f"Invalid log level: {v}. Must be one of: {', '.join(valid_levels)}"
            )
        return v_upper

    model_config = SettingsConfigDict(
        env_file=environ.get("ENV_FILE", "/opt/cysl/api/.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # REQUIRED in Docker/K8s
    )


def get_settings() -> Settings:
    return Settings()
