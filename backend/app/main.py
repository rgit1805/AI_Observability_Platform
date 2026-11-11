from fastapi import FastAPI
from app.api.routes.models import router as models_router

app = FastAPI(
    title="Aegis AI",
    description="Unified AI Observability Platform",
    version="0.1.0"
)

app.include_router(
    models_router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Aegis AI",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }