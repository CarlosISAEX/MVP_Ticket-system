# backend/tests/conftest.py
import os
import importlib

# 1) Forzar entorno de pruebas y SQLite (sin depender de Docker)
if os.path.exists(".env.test"):
    from dotenv import load_dotenv
    load_dotenv(".env.test", override=True)
else:
    os.environ.setdefault("APP_ENV", "test")
    os.environ.setdefault("DATABASE_URL", "sqlite:///./tests_tmp.db")

# 2) Recargar módulos que leen settings en el import
import backend.app.core.config as config
importlib.reload(config)
import backend.app.db.session as session_mod
importlib.reload(session_mod)
