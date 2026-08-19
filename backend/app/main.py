import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.admin import router as admin_router
from app.api.leads import router as leads_router
from app.config import settings
from app.db import ensure_schema, pool

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if not settings.admin_password:
        log.warning("ADMIN_PASSWORD не задан — вход в админку будет невозможен")
    ensure_schema()
    yield
    pool.close()


app = FastAPI(title=settings.app_name, lifespan=lifespan, docs_url=None, redoc_url=None)

# В продакшене фронт и API за одним nginx (same-origin); CORS нужен только
# при прямом обращении к API с vite dev-сервера в обход прокси.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(leads_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
