# backend/app/api/routes/tickets.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.ticket import Ticket
from backend.app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from backend.app.crud import ticket as crud_ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/", response_model=list[TicketRead])
def list_tickets(db: Session = Depends(get_db)):
    return crud_ticket.list_tickets(db)


@router.post("/", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    return crud_ticket.create_ticket(db, payload)


@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    t = crud_ticket.update_ticket(db, ticket_id, payload)
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return t
