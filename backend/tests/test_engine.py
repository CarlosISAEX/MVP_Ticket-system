# backend/tests/test_engine.py
from backend.app.db.session import engine
from sqlalchemy import inspect, text

def test_engine_and_tables():
    print("Engine URL ->", engine.url)
    insp = inspect(engine)
    assert insp.has_table("users") is not None  # o quita si aún no tienes users

    with engine.connect() as c:
        if c.dialect.name == "sqlite":
            v = c.execute(text("select sqlite_version()")).fetchone()[0]
            print("sqlite_version:", v)
        else:  # Postgres, etc.
            db, schema = c.execute(
                text("select current_database(), current_schema()")
            ).fetchone()
            print("DB:", db, "Schema:", schema)

        # alembic_version opcional
        try:
            av = c.execute(text("select version_num from alembic_version")).scalar()
            print("alembic_version:", av)
        except Exception as e:
            print("alembic_version not found:", e)
