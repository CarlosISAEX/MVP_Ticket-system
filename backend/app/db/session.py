from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from backend.app.core.config import settings

# Engine de conexión
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # valida la conexión antes de usarla
    future=True              # usa la API 2.0 de SQLAlchemy
)

# SessionLocal: factoría de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Dependencia de FastAPI para inyectar la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
