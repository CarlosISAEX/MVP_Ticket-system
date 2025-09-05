# backend/tests/test_smoke.py
import types
import uuid
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session
import pytest

from backend.app.core.config import settings
from backend.app.db.session import engine, SessionLocal, get_db
from backend.app.models.user import User


def test_settings_basic_loaded():
    # Ajusta/añade claves si quieres validar más configuración
    assert settings.DATABASE_URL, "DATABASE_URL no está configurada"
    assert isinstance(getattr(settings, "APP_NAME", ""), str), "APP_NAME no es str"
    # CORS puede ser lista o str parseada; valida que exista
    assert hasattr(settings, "CORS_ORIGINS"), "Falta CORS_ORIGINS en settings"


def test_engine_connects():
    with engine.connect() as conn:
        assert conn.execute(text("SELECT 1")).scalar() == 1


def test_sessionlocal_and_dependency():
    # SessionLocal directa
    db = SessionLocal()
    try:
        assert isinstance(db, Session)
        assert db.execute(text("SELECT 1")).scalar() == 1
    finally:
        db.close()

    # Dependencia get_db()
    dep = get_db()
    assert isinstance(dep, types.GeneratorType)
    db2 = next(dep)
    try:
        assert isinstance(db2, Session)
        assert db2.execute(text("SELECT 1")).scalar() == 1
    finally:
        try:
            next(dep)  # cierra el generator -> hace db.close()
        except StopIteration:
            pass


def test_user_model_mapping():
    mapper = inspect(User)
    cols = mapper.columns
    for name in ["id", "email", "hashed_password", "role", "created_at"]:
        assert name in cols, f"Columna {name} no mapeada"

    assert cols["id"].primary_key is True
    assert cols["email"].nullable is False and cols["email"].unique is True
    assert cols["role"].nullable is False
    assert cols["created_at"].nullable is False


@pytest.mark.integration
def test_user_roundtrip_if_table_exists():
    # Este test solo corre si ya aplicaste migraciones (tabla 'users' creada)
    insp = inspect(engine)
    if not insp.has_table("users"):
        pytest.skip("Tabla 'users' no existe. Corre: alembic upgrade head")

    db = SessionLocal()
    try:
        # ⚠️ No haremos commit: todo se descarta al cerrar la sesión.
        unique_email = f"smoke_{uuid.uuid4().hex[:12]}@example.com"
        u = User(email=unique_email, hashed_password="x")
        db.add(u)
        # Consulta dentro de la misma sesión/transacción
        fetched = db.query(User).filter_by(email=unique_email).first()
        assert fetched is not None, "No pudo leerse el usuario insertado"
        assert fetched.role == "user", "Default 'user' no aplicado"
        assert fetched.created_at is not None, "created_at no seteado"
    finally:
        # rollback implícito al no hacer commit
        db.close()

