from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .db import engine, Base
from . import models
from .routers import auth as auth_router 
from .routers import animals as animal_router
from .routers import adoptions 
from .routers import reactions



app = FastAPI(
    title="AdoCÃO API",
    description="API para sistema de adoção de animais",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Garante que as tabelas existem
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔹 Aqui a mágica: registra as rotas do módulo auth
app.include_router(auth_router.router)
app.include_router(animal_router.router)
app.include_router(adoptions.router)
app.include_router(reactions.router)
