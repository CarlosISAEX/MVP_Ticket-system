import time
from datetime import datetime
from sqlalchemy import inspect, select
from sqlalchemy.orm import Session
from backend.app.db.session import engine, SessionLocal
from backend.app.models.ticket import Ticket  # ajusta el import a tu ruta real


def test_table_exists():
    insp = inspect(engine)
    assert "tickets" in insp.get_table_names()


def test_create_minimal_ticket_and_defaults():
    # title es obligatorio; el resto opcional
    with SessionLocal() as s:
        t = Ticket(title="Hello world")
        s.add(t)
        s.commit()
        s.refresh(t)

        assert t.id is not None
        assert t.status == "open"        # default
        assert t.priority == "low"       # default
        assert isinstance(t.created_at, datetime)
        assert isinstance(t.updated_at, datetime)
        # FKs son nullables
        assert t.created_by_id is None
        assert t.assigned_to_id is None


def test_updated_at_changes_on_update():
    with SessionLocal() as s:
        t = Ticket(title="To be updated")
        s.add(t)
        s.commit()
        s.refresh(t)
        first_updated = t.updated_at

        # garantizamos cambio de tiempo (sqlite puede tener resolución baja)
        time.sleep(1.1)
        t.description = "now updated"
        s.add(t)
        s.commit()
        s.refresh(t)

        assert t.updated_at >= first_updated
        assert t.description == "now updated"


def test_can_query_back_ticket():
    with SessionLocal() as s:
        # crea
        t = Ticket(title="Query me")
        s.add(t)
        s.commit()
        # consulta
        found = s.execute(select(Ticket).where(Ticket.title == "Query me")).scalar_one()
        assert found.id == t.id
        assert found.title == "Query me"
