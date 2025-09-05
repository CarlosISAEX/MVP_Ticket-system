# backend/tests/test_db.py

from sqlalchemy import text
from backend.app.db.session import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
import types


def test_engine_connects_and_executes_select_1():
    """Prueba que el engine pueda conectarse y ejecutar SELECT 1"""
    with engine.connect() as conn:
        value = conn.execute(text("SELECT 1")).scalar()
        assert value == 1


def test_sessionlocal_creates_session_and_closes():
    """Prueba que SessionLocal cree y cierre correctamente una sesión"""
    db = SessionLocal()
    try:
        assert isinstance(db, Session)
        value = db.execute(text("SELECT 1")).scalar()
        assert value == 1
    finally:
        db.close()


def test_get_db_dependency_yields_session_and_closes():
    """Prueba que la dependencia get_db genere y cierre la sesión"""
    dep = get_db()
    assert isinstance(dep, types.GeneratorType)
    db = next(dep)
    try:
        assert isinstance(db, Session)
        value = db.execute(text("SELECT 1")).scalar()
        assert value == 1
    finally:
        try:
            next(dep)
        except StopIteration:
            pass
