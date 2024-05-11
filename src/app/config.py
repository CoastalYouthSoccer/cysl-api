from os import environ
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    auth0_algorithms: str
    database_url: str
    log_level: int = 30

    class Config:
        env_file = environ.get("ENV_FILE", ".env")

def get_settings():
    return Settings()
