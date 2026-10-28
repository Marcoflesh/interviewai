# Bitácora (más reciente arriba). Una entrada por sesión de trabajo.

## 2026-10-28 — Sesión 2: Ollama + UI + GitHub Pages (Claude)
**Hecho:** `OllamaLLM` + `list_ollama_models` (`services/llm_client.py`), `LLMUnavailableError` → HTTP 503, modelo por sesión (`StartSessionRequest.model`), `/api/llm/status`, CORS configurable (`CORS_ORIGINS`), UI con URL del backend y selector de modelo, mensaje de espera, workflow de Pages, `.env.example` orientado a Ollama, `host.docker.internal` en compose, `tests/test_ollama.py`.
**Verificado:** ver pytest de esta sesión (servidor Ollama simulado). **NO verificado:** Ollama real, calidad del JSON de modelos pequeños, latencia, GitHub Pages desplegado, HTTPS→localhost en Safari (probablemente bloqueado; usar Chrome/Edge/Firefox).
**Siguiente:** correr con Ollama real, ajustar prompts al modelo elegido (T-302), medir latencia (T-303).

## 2026-10-28 — Sesión 1: esqueleto inicial (Claude)
**Entrada:** SRS de InterviewAI (`docs/SRS.md`, copiado sin las imágenes base64 de los diagramas).
**Hecho**
- Estructura del repo, `AGENTS.md`, `HANDOFF.md`, ROADMAP (7 fases, IDs T-xxx), ARCHITECTURE, DECISIONS (D-01…D-12), TRACEABILITY.
- Backend: `core/` (constantes, RBAC, monitor), `services/` (features, anonymizer, llm_client+FakeLLM, report, stats, session_store), `schemas/`, `agents/` (state, prompts, evaluator, interviewer, graph), `api/` (sessions funcionales; stubs 501 para RF-07..13), `db/models.py`, `cli_demo.py`.
- MLOps: `mlops/evaluate_golden.py` + CSV de ejemplo (inventado).
- Frontend: vista estudiante (setup, chat, panel STAR), reporte con CSS de impresión + CSAT; `po.html` y `admin.html` son stubs.
- Infra: `docker-compose.yml`, Dockerfiles (Python 3.12.7 fijo), `.env.example`, `Makefile`.
**Verificado:** `pytest` → 31 passed (Python 3.12.3, langgraph 1.2.18, fastapi 0.162.0). Sintaxis JS con `node --check`. Modelos crean 8 tablas en SQLite. Gate RN-07 corre y rechaza FakeLLM (esperado).
**NO verificado:** Docker, navegador, CORS, Postgres, cualquier LLM real.
**Problemas encontrados:** el shell del sandbox es `sh` (sin llaves `{a,b}`); no afecta al proyecto.
**Siguiente:** T-001 → T-301 → T-107/T-108 (ver HANDOFF).
