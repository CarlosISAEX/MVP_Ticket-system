from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from app.api import tickets
from backend.app.api import tickets
from dotenv import load_dotenv;load_dotenv()  # carga .env del dir raiz 


#from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings

#app = FastAPI()

app = FastAPI(title="Ticket System")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])

@app.get("/")
def root():
    return {"message": "Ticket System API running 🚀"}
