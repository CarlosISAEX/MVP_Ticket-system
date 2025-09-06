
# backend/migrations/env.py

import os
import sys
from pathlib import Path
from logging.config import fileConfig
from alembic import context

# --- Rutas correctas desde backend/migrations ---
CURRENT_DIR = Path(__file__).resolve().parent           # .../backend/migrations
REPO_ROOT = CURRENT_DIR.parents[1]                       # .../ (raíz del repo)

# Si prefieres ser explícito: CURRENT_DIR.parents[2] => subir dos niveles (migrations -> backend -> repo)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
# --- Asegura que el import 'backend.*' funcione ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, "."))  # raíz del repo
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Carga .env (o .env.test si existe) ANTES de importar settings/engine
try:
    from dotenv import load_dotenv
    if os.path.exists(".env.test"):
        load_dotenv(".env.test", override=True)
    else:
        load_dotenv(override=True)
except Exception:
    # dotenv es opcional; si no existe, seguimos
    pass

# Importa configuración y metadata de tu app
from backend.app.db.session import engine  # usa el mismo engine de la app
from backend.app.db.base import Base       # tu declarative Base

# ⬇⬇⬇ MUY IMPORTANTE: importa los módulos de modelos para que Alembic los registre
# Importa aquí todos los modelos que quieras que aparezcan en autogenerate:
from backend.app.models import user  # p.ej. users
# Si tienes más (ticket, comment, etc.), impórtalos también:
from backend.app.models import ticket #comment

# Config de Alembic
config = context.config

# Logging (opcional)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata objetivo para autogenerate
target_metadata = Base.metadata


def get_url() -> str:
    # Toma la URL desde tu engine real (garantiza que sea la misma que usa la app)
    return str(engine.url)


def include_object(object, name, type_, reflected, compare_to):
    """
    Puedes filtrar objetos aquí si quieres excluir tablas/esquemas.
    Por defecto, incluye todo.
    """
    return True


def run_migrations_offline() -> None:
    """Migrations en modo 'offline' (genera SQL sin conectar)."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=True,             # detecta cambios de tipo
        compare_server_default=True,   # detecta server_default
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Migrations en modo 'online' (conexión real a la DB)."""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True,
            compare_server_default=True,
            render_as_batch="sqlite" in str(connectable.url),  # útil para SQLite
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
