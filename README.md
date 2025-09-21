# Ticket System API

Ticket Management System built with FastAPI, SQLAlchemy, and PostgreSQL, containerized with Docker Compose.  

---

## Features
- FastAPI backend with automatic Swagger UI at `/docs`.
- SQLAlchemy ORM with Alembic migrations.
- JWT authentication.
- Environment-based configuration via `.env`.
- Docker Compose setup (API + PostgreSQL + Adminer).

---

## Requirements
- Python 3.11+
- PostgreSQL (local or Docker)
- Docker & Docker Compose (recommended)
- Poetry or pip/venv for dependencies

---

## Setup

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
Copy `.env.example` → `.env` and adjust values:
```bash
cp .env.example .env
```

---

## Run with Docker
```bash
docker compose up -d
```

Services available:
- API → http://localhost:8000  
- Swagger UI → http://localhost:8000/docs  
- Adminer → http://localhost:8080 (use Postgres credentials)  

---

## Project Structure (simplified)
```
MVP_Ticket-system/
│── backend/
│   ├── app/              # FastAPI app modules
│   ├── migrations/       # Alembic migrations
│── docker-compose.yml
│── requirements.txt
│── .env.example
│── README.md
```

---
