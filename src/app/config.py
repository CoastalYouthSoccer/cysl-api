from os import environ
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    management_auth0_domain: str
    management_auth0_client_id: str
    management_auth0_client_secret: str

    auth0_algorithms: str = "RS256"

    database_url: str
    celery_database_url: str

    log_level: str = "INFO"

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

    @field_validator('otel_insecure', mode='before')
    @classmethod
    def parse_bool(cls, v):
        """Parse boolean from string"""
        print(f"DEBUG: otel_insecure raw value: {v!r} (type: {type(v).__name__})")
    
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            v = v.strip().strip('"').strip("'")
            result = v.lower() in ('true', '1', 'yes', 'on')
            print(f"DEBUG: Parsed to: {result}")
            return result
        return bool(v)

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
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()
