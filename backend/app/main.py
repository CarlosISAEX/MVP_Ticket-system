from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from app.api import tickets
from backend.app.api import tickets
app = FastAPI(title="Ticket System")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])

@app.get("/")
def root():
    return {"message": "Ticket System API running 🚀"}
