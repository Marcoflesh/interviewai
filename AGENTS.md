# Instrucciones para cualquier IA / desarrollador que retome este repo

1. Lee, en este orden: **`HANDOFF.md`** (estado actual y qué sigue) → `docs/ROADMAP.md` → `docs/DECISIONS.md`.
2. El **SRS** (`docs/SRS.md`) es la fuente de verdad de requisitos. No cambies umbrales/valores de `backend/app/core/constants.py` sin actualizar `docs/DECISIONS.md`.
3. Antes de tocar nada: `make test` debe estar en verde.
4. Al terminar CADA tarea, actualiza: estado en `docs/ROADMAP.md`, fila en `docs/TRACEABILITY.md`, una entrada nueva (arriba) en `docs/WORKLOG.md` y la sección "Estado actual" de `HANDOFF.md`.
5. Documenta en el código: docstring con los IDs del SRS (RF-xx / RN-xx / RNF-xx) y `TODO (ROADMAP T-xxx)` donde falte algo.
6. Dependencias con versión exacta (RN-12). Nada de secretos en git. Identificadores en inglés; estados del SRS en español (`profundizar_pregunta`, etc.).
