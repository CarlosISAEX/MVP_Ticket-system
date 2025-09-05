# 🎫 Ticket System API (MVP)

This is the minimal viable product (MVP) of the Ticket System API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, designed to be containerized with **Docker Compose**.

---

## 🚀 Features
- FastAPI backend with automatic Swagger UI (`/docs`).
- SQLAlchemy ORM with Alembic migrations.
- Environment-based configuration using `.env`.
- JWT authentication (configurable).
- SQLite support for unit tests.
- Docker Compose setup (API + Postgres + Adminer).

---

## ⚙️ Requirements
- Python 3.11+
- PostgreSQL (local or Docker)
- Docker & Docker Compose (recommended)
- Poetry or pip/venv for dependencies

---

## 🛠️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/CarlosISAEX/MVP_Ticket-system.git
cd MVP_Ticket-system
```

### 2. Create and activate virtualenv
```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows PowerShell
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment variables
Copy `.env.example` to `.env` and adjust values:
```bash
cp .env.example .env
```

---

## 🐳 Run with Docker

```bash
docker compose up -d
```

Services:
- **API** → http://localhost:8000
- **Swagger** → http://localhost:8000/docs
- **Adminer** → http://localhost:8080 (login with Postgres credentials)

---

## 🧪 Testing (SQLite by default + Postgres option)

By default, tests run **without Docker or Postgres**. They use **SQLite** for speed and isolation.  
This is enforced via `backend/tests/conftest.py`:

```env
APP_ENV=test
DATABASE_URL=sqlite:///./tests_tmp.db
```

### ✅ Run tests
```bash
pytest -q
```

### 🔍 Verify SQLite is used
One test asserts:  
```python
assert engine.dialect.name == "sqlite"
```

### 🔁 Override DATABASE_URL (e.g. custom SQLite file)
```bash
# Linux/Mac
export DATABASE_URL="sqlite:///./custom_tests.db"
pytest -q

# Windows PowerShell
$env:DATABASE_URL="sqlite:///./custom_tests.db"
pytest -q
```

### 🧪 Integration tests against Postgres
1. Start Docker services:
```bash
docker compose up -d
```

2. Point tests to Postgres:
```bash
# Linux/Mac
export DATABASE_URL="postgresql+psycopg://appuser:apppass@localhost:5432/tickets"
pytest -q

# Windows PowerShell
$env:DATABASE_URL="postgresql+psycopg://appuser:apppass@localhost:5432/tickets"
pytest -q
```

> If running tests **inside the API container**, use `host=db`:
> ```
> postgresql+psycopg://appuser:apppass@db:5432/tickets
> ```

### 🧹 Clean up test artifacts
```bash
rm -f tests_tmp.db  # Linux/Mac
Remove-Item -Force tests_tmp.db  # PowerShell
```

### 📦 Migrations in tests
For minimal connectivity tests (`SELECT 1`), **no migrations are required**.  
If testing actual models, run migrations first:
```bash
alembic upgrade head
```
Or use a pytest fixture that creates/drops tables in SQLite in-memory.

---

## 📜 License
MIT License
