from fastapi import FastAPI

from .db import engine, Base
from . import models
from .routers import auth as auth_router 
from .routers import animals as animal_router
from .routers import adoptions as adoption_router



app = FastAPI(
    title="AdoCÃO API",
    description="API para sistema de adoção de animais",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    # Garante que as tabelas existem
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


# 🔹 Aqui a mágica: registra as rotas do módulo auth
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(animal_router.router)
app.include_router(adoption_router.router)