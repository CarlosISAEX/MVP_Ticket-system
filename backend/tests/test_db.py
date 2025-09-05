# backend/tests/test_db.py
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.app.db.session import engine, SessionLocal, get_db
import types


def test_engine_uses_sqlite_in_tests():
    # confirmamos que el dialecto es sqlite durante los tests
    assert engine.dialect.name == "sqlite"


def test_engine_connects_and_executes_select_1():
    with engine.connect() as conn:
        assert conn.execute(text("SELECT 1")).scalar() == 1


def test_sessionlocal_creates_session_and_closes():
    db = SessionLocal()
    try:
        assert isinstance(db, Session)
        assert db.execute(text("SELECT 1")).scalar() == 1
    finally:
        db.close()


def test_get_db_dependency_yields_session_and_closes():
    dep = get_db()
    assert isinstance(dep, types.GeneratorType)
    db = next(dep)
    try:
        assert isinstance(db, Session)
        assert db.execute(text("SELECT 1")).scalar() == 1
    finally:
        try:
            next(dep)  # debe cerrar y lanzar StopIteration
        except StopIteration:
            pass
