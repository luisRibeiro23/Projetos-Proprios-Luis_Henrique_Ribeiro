from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .db import engine, Base
from . import models  # garante que os models sejam registrados
from .routers import auth as auth_router
from .routers import animals as animal_router
from .routers import adoptions
from .routers import reactions

# =====================================================
# App
# =====================================================

app = FastAPI(
    title="AdoCÃO API",
    description="API para sistema de adoção de animais",
    version="1.0.0",
)

# =====================================================
# CORS
# =====================================================
# ⚠️ Quando publicar o frontend (Netlify/Vercel),
# adicione aqui o domínio real do site.
# Exemplo:
# "https://adocao.netlify.app",

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://stately-cajeta-17b2b6.netlify.app",
]




app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# Startup
# =====================================================

@app.on_event("startup")
def on_startup():
    # Garante que as tabelas existem
    Base.metadata.create_all(bind=engine)

# =====================================================
# Healthcheck (Render usa isso às vezes)
# =====================================================

@app.get("/health")
def health():
    return {"status": "ok"}

# =====================================================
# Static files (imagens dos animais)
# =====================================================
# IMPORTANTE:
# - No Render, Root Directory deve ser "adocao"
# - A pasta "static/" deve estar dentro de "adocao/"

app.mount("/static", StaticFiles(directory="static"), name="static")

# =====================================================
# Routers
# =====================================================

app.include_router(auth_router.router)
app.include_router(animal_router.router)
app.include_router(adoptions.router)
app.include_router(reactions.router)
