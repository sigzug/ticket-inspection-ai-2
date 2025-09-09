# config/settings_schema.py
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Core
    DEBUG: bool = False
    SECRET_KEY: str
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    # DB (bytt til Postgres enkelt via env)
    DB_ENGINE: Literal["sqlite", "postgres"] = "sqlite"
    DATABASE_URL: str | None = None  # f.eks. postgres://user:pwd@host:5432/db

    # Django
    TIME_ZONE: str = "Europe/Oslo"
    LANGUAGE_CODE: str = "nb"


settings = Settings()  # laster fra .env automatisk
