#backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv; load_dotenv()

from backend.app.core.config import settings
from backend.app.api import api_router

app = FastAPI(title="Ticket System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Salud simple
@app.get("/health")
def health():
    return {"status": "ok"}

#app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router, prefix=f"{settings.API_PREFIX}/v1")

@app.get("/")
def root():
    return {"message": "Ticket System API running 🚀"}
