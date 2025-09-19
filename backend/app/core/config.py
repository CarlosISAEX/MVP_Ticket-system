## backend/core/config.py
from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import json

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",  # puedes dejarlo o quitarlo si ya declaras todo
    )

    APP_NAME: str = "Ticket System API"
    APP_ENV: str = "development"
    API_PREFIX: str = "/api"
    # En ejecución normal se sobrescribe con la variable DATABASE_URL de .env
    DATABASE_URL: str #= "postgresql+psycopg:///tickets"

    # Nuevas que tu .env ya tiene:
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    SECRET_KEY: str = "changeme"

    # JWT (usa los nombres “preferidos” y deja compat si quieres)
    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Compatibilidad opcional (fallback)
    @field_validator("JWT_SECRET", mode="before")
    @classmethod
    def _jwt_secret_compat(cls, v):
        import os
        return v or os.getenv("JWT_SECRET_KEY")

    @field_validator("JWT_ALG", mode="before")
    @classmethod
    def _jwt_alg_compat(cls, v):
        import os
        return v or os.getenv("JWT_ALGORITHM")

    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES", mode="before")
    @classmethod
    def _jwt_exp_compat(cls, v):
        import os
        return v or os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _parse_cors(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return []
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                import json
                return json.loads(s)
            return [item.strip() for item in s.split(",") if item.strip()]
        if isinstance(v, (list, tuple)):
            return list(v)
        raise TypeError("CORS_ORIGINS debe ser lista o string")

settings = Settings()
