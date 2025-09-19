# backend/app/schemas/ticket.py

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class TicketCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None

class TicketRead(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    created_by_id: int | None
    assigned_to_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # Pydantic v2

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to_id: Optional[int] = None
    created_by_id: Optional[int] = None