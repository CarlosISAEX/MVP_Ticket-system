#backend/app/api/init.py
from fastapi import APIRouter
from backend.app.api.routes.tickets import router as tickets_router

api_router = APIRouter()
api_router.include_router(tickets_router)
