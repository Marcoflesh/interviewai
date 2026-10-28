# InterviewAI — Simulador inteligente de entrevistas laborales

Plataforma web donde un **Agente Entrevistador** y un **Agente Evaluador** (LLM, orquestados con **LangGraph**) simulan entrevistas, califican cada respuesta en método **STAR** (1–5) y generan un reporte final con Plan de Acción. Backend Python/FastAPI, frontend HTML/CSS, PostgreSQL, todo en **Docker**. Requisitos completos: [`docs/SRS.md`](docs/SRS.md).

> Estado: **esqueleto funcional** (núcleo + grafo + API + frontend base con LLM falso). Ver [`HANDOFF.md`](HANDOFF.md).

## Probar sin Docker ni API keys (FakeLLM)
```bash
cd backend && pip install -r requirements-dev.txt
make test          # 31 pruebas
make demo          # entrevista en terminal
uvicorn app.main:app --reload   # API en :8000  (docs en /docs)
# frontend: abrir frontend/index.html con un servidor estático, p. ej. `python -m http.server 8080 -d frontend`
```
## Con Docker (pendiente de validar, ver T-001)
`make up` → frontend http://localhost:8080 · API http://localhost:8000

## Mapa del repo
| Ruta | Contenido |
|---|---|
| `backend/app/agents/` | Grafo LangGraph (`graph.py`), Entrevistador, Evaluador, prompts |
| `backend/app/services/` | features (Regex), anonimizador, LLM client, reporte, stats |
| `backend/app/api/` · `schemas/` · `db/` | Endpoints, contratos, modelos SQLAlchemy |
| `mlops/` | Validación contra Golden Dataset (RN-07), compatible con Colab |
| `frontend/` | Vistas HTML/CSS/JS (estudiante, reporte; PO y admin pendientes) |
| `docs/` | SRS, roadmap, arquitectura, trazabilidad, decisiones, bitácora |
