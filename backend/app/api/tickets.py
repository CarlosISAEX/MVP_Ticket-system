from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_tickets():
    return [{"id": 1, "title": "Primer ticket"}]

@router.post("/")
def create_ticket(title: str):
    return {"id": 2, "title": title}
