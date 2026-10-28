"""Punto de entrada FastAPI. Ejecutar: uvicorn app.main:app --reload (o docker compose up)."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import sessions, stubs
from app.core.monitor import format_monitor

app = FastAPI(title="InterviewAI", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8080"], allow_methods=["*"], allow_headers=["*"])
app.include_router(sessions.router)
app.include_router(stubs.router)


@app.get("/health")
def health():
    return {"status": "ok", "json_format_error_rate": format_monitor.error_rate}
