# tests/test_settings.py
from backend.app.core.config import settings

def test_env_loaded():
    # al menos debe existir la URL por defecto o la del .env
    assert settings.DATABASE_URL, "DATABASE_URL no cargó"
