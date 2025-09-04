# backend/app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg:///tickets"
    API_PREFIX: str = "/api"
    CORS_ORIGINS: str = "http://localhost:5173"

    # Configuración para que lea el .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
