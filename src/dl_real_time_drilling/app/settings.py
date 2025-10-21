from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Secrets only; non-secrets live in configs/*
    MLFLOW_TRACKING_URI: str | None = None
    MLFLOW_REGISTRY_URI: str | None = None
    MLFLOW_TRACKING_TOKEN: str | None = None
    MLFLOW_S3_ENDPOINT_URL: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=None, extra="ignore")


SETTINGS = Settings()



