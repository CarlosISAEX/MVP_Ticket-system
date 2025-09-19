# backend/app/crud/ticket.py
from __future__ import annotations

from typing import Optional, Iterable
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from backend.app.models.ticket import Ticket
from backend.app.schemas.ticket import TicketCreate  # TicketUpdate es opcional (ver notas abajo)


def _to_dict_exclude_unset(model) -> dict:
    """
    Compat Pydantic v1/v2: obtiene dict solo con campos enviados (exclude_unset=True).
    """
    if hasattr(model, "model_dump"):
        # Pydantic v2
        return model.model_dump(exclude_unset=True)
    # Pydantic v1
    return model.dict(exclude_unset=True)


def create_ticket(db: Session, data: TicketCreate) -> Ticket:
    """
    Crea un ticket. Usa solo campos que existen en tu TicketCreate actual (title, description).
    Si en el futuro agregas 'priority' al schema, también se tomará automáticamente.
    """
    payload = _to_dict_exclude_unset(data)

    # Asegurar claves válidas según tu modelo actual
    allowed: Iterable[str] = ("title", "description", "status", "priority", "created_by_id", "assigned_to_id")
    filtered = {k: v for k, v in payload.items() if k in allowed}

    # title y description ya están en tu TicketCreate; priority es opcional (modelo tiene default "low")
    t = Ticket(**filtered)

    try:
        db.add(t)
        db.commit()
        db.refresh(t)
        return t
    except IntegrityError:
        db.rollback()
        # Por si en el futuro haces title único u otras constraints
        raise
    except Exception:
        db.rollback()
        raise


def list_tickets(db: Session) -> list[Ticket]:
    """
    Lista todos los tickets (más recientes primero).
    Nota: la paginación la manejas en la capa de rutas si la necesitas.
    """
    return db.query(Ticket).order_by(Ticket.created_at.desc()).all()


def update_ticket(db: Session, ticket_id: int, data) -> Optional[Ticket]:
    """
    Actualiza campos del ticket. 'data' debe ser un modelo tipo TicketUpdate
    (todos los campos opcionales). Es compatible con Pydantic v1/v2.
    Devuelve None si el ticket no existe.
    """
    t: Optional[Ticket] = db.get(Ticket, ticket_id)
    if not t:
        return None

    payload = _to_dict_exclude_unset(data)

    # Campos permitidos a actualizar (evita tocar id/created_at/updated_at)
    allowed_updates: set[str] = {
        "title",
        "description",
        "status",
        "priority",
        "assigned_to_id",
        "created_by_id",
    }
    for field, value in payload.items():
        if field in allowed_updates:
            setattr(t, field, value)

    try:
        db.add(t)
        db.commit()
        db.refresh(t)
        return t
    except IntegrityError:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise
