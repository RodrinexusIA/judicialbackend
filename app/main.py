from fastapi import FastAPI

from app.api.routers import health, jobs, processos
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine

setup_logging()

app = FastAPI(title="Judicial Backend MVP")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(health.router, tags=["health"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(processos.router, prefix="/processos", tags=["processos"])
