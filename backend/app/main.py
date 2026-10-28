"""Punto de entrada FastAPI. Ejecutar: uvicorn app.main:app --reload (o docker compose up)."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import sessions, stubs
from app.config import settings
from app.core.monitor import format_monitor
from app.services.llm_client import LLMUnavailableError, list_ollama_models

app = FastAPI(title="InterviewAI", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in settings.cors_origins.split(",")], allow_methods=["*"], allow_headers=["*"])
app.include_router(sessions.router)
app.include_router(stubs.router)


@app.get("/health")
def health():
    return {"status": "ok", "json_format_error_rate": format_monitor.error_rate}


@app.get("/api/llm/status")
def llm_status():
    """La UI lo usa para mostrar si Ollama esta vivo y que modelos hay instalados."""
    if settings.llm_provider != "ollama":
        return {"provider": settings.llm_provider, "ok": True, "models": [], "default": None}
    try:
        return {"provider": "ollama", "ok": True, "models": list_ollama_models(settings.ollama_base_url),
                "default": settings.llm_model or None}
    except LLMUnavailableError as exc:
        return {"provider": "ollama", "ok": False, "models": [], "default": None, "detail": str(exc)}
