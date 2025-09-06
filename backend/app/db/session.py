# backend/app/db/session.py
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings
from .base import Base

DATABASE_URL = settings.DATABASE_URL

# Configuración especial para SQLite (necesario en pruebas y desarrollo ligero)
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Engine de conexión
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # valida la conexión antes de usarla
    connect_args=connect_args,
    future=True,             # activa la API 2.0 de SQLAlchemy
)

# SessionLocal: factoría de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # evita que expiren los objetos después de commit
    future=True,
)

# Dependencia de FastAPI para inyectar la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
