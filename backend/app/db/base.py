# backend/app/db/base.py
from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Convención de nombres estable para constraints/índices (útil para Alembic)
naming_convention = {
    "ix": "ix_%(table_name)s_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)

class Base(DeclarativeBase):
    metadata = metadata

# Importa modelos para que queden registrados en Base.metadata (autogenerate de Alembic)
# Se envuelve en try/except para evitar problemas de importación circular en ciertos contextos.
try:
    from backend.app.models.user import User     # noqa: F401
    from backend.app.models.ticket import Ticket # noqa: F401
except Exception:
    pass

__all__ = ["Base", "metadata"]
