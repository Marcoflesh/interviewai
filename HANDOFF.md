# HANDOFF — leer primero (para IA auxiliar o persona que retome)

**Proyecto:** InterviewAI (SRS en `docs/SRS.md`). **Autor/dueño:** Marco (habla español; registro casual). **Última actualización:** 2026-10-28.

## Estado actual
- **Hecho y probado (31 pruebas en verde, `make test`):** constantes del SRS, features Regex, esquema JSON del evaluador, RBAC (modelo), anonimizador v0, grafo LangGraph completo (profundizar / siguiente / finalizar), Evaluador con reintento, Entrevistador, `FakeLLM`, reporte (2 respuestas débiles, plan de acción), estadística del gate RN-07, API FastAPI con almacén en memoria, modelos SQLAlchemy (crean tablas en SQLite).
- **Hecho pero SIN verificar:** `Dockerfile`s y `docker-compose.yml` (nunca construidos), frontend (solo se comprobó la sintaxis JS; **no se abrió en navegador**), CORS entre :8080 y :8000.
- **No existe:** LLM real (stubs Gemini/OpenAI), Postgres conectado/migraciones, auth real, PDF desde backend, Golden Dataset real (el CSV es de ejemplo inventado), paneles PO/Admin/Analista, auditoría de sesgos.
- **Dato importante:** con `FakeLLM` el gate de RN-07 **falla** (Spearman 0.58 < 0.75). Es lo esperado: FakeLLM no es un modelo real.

**Actualización 2026-10-28 (sesión 2):** `OllamaLLM` implementado (probado solo contra servidor simulado; **nunca contra Ollama real**), selector de modelo en la UI, `/api/llm/status`, CORS para GitHub Pages y workflow `.github/workflows/pages.yml`. T-301 pasa a 🔄 (falta correr con Ollama real y medir calidad/JSON).

## Qué hacer ahora (en orden)
1. **T-001** Probar `docker compose up --build`, corregir lo que falle.
2. **T-301** Implementar `GeminiLLM` u `OpenAILLM` en `backend/app/services/llm_client.py` (salida JSON; respetar `parse_evaluation`).
3. **T-107 / T-108** Alembic + `PostgresSessionStore`.
4. **T-303** Medir y bajar latencia a < 2.5 s por turno.
5. **T-401 / T-402** Reporte con catálogo real y PDF desde backend.
Detalle de todas las tareas: `docs/ROADMAP.md`.

## Protocolo de reanudación
1. `cd backend && pip install -r requirements-dev.txt && python -m pytest -q` → debe dar 31 passed.
2. Lee `docs/DECISIONS.md` (las suposiciones donde el SRS es ambiguo; D-05 y D-02 requieren confirmación).
3. Toma la primera tarea ⬜ de la lista de arriba. Escribe la prueba primero cuando sea lógica determinista.
4. Al terminar: actualiza `docs/ROADMAP.md`, `docs/TRACEABILITY.md`, agrega entrada en `docs/WORKLOG.md` (arriba) y edita "Estado actual" aquí.

## Reglas que no se rompen
- Los valores del SRS (umbral 3, 1–5, 5–10 respuestas, 0.75, 2.5 s, 8 s, 0.5 %) viven en `core/constants.py`; no los dupliques.
- La lógica de decisión del grafo es **determinista** y se prueba sin LLM; el LLM siempre va detrás de `LLMClient`.
- Todo CV pasa por `anonymize()` antes de guardarse (RN-10).
- Python y dependencias con versión exacta (RN-12). Versiones actuales probadas: ver `backend/requirements.txt`.
- No inventes resultados: si algo no se probó, dilo en `WORKLOG.md`.

## Comandos útiles
`make test` · `make demo` (entrevista en terminal) · `make golden` · `make up` · API docs en http://localhost:8000/docs
