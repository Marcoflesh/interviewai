# Arquitectura

```
 Navegador (HTML/CSS/JS) ──HTTP/JSON──> FastAPI (backend) ──> LangGraph (grafo por turno)
        │ nginx :8080                     │ :8000              ├─ Agente Entrevistador ─┐
        │                                 │                    └─ Agente Evaluador ─────┴─> LLMClient ─> Gemini/OpenAI (RIN-01)
        │                                 └──> PostgreSQL (RIN-02)   [hoy: store en memoria]
        └── red interna Docker `interviewai_net` (RIN-04)
 Colab ──> mlops/evaluate_golden.py ──> Golden Dataset (RIN-03)
```

## Grafo (un `invoke` = un turno) — `backend/app/agents/graph.py`
```
START ─(sin respuesta)→ generar_primera_pregunta → END
START ─(con respuesta)→ extraer_features → evaluar_respuesta ─┬→ profundizar_pregunta ──→ END   (RN-03)
                                                              ├→ pasar_a_siguiente_tema → END   (RN-05)
                                                              └→ finalizar_entrevista ──→ END   (nodo terminal)
```
Prioridad de la arista condicional (`route_after_eval`): (1) `answered_count >= max_turns` → finalizar; (2) Acción<3 o Resultado<3 y no estamos en seguimiento → profundizar; (3) siguiente tema.
El reporte (RF-05) lo invoca la capa API cuando `status == finalizar_entrevista`.

## Separación determinista / probabilístico (idea central del SRS)
- **Determinista (testeable sin LLM):** features Regex (RN-04), validación de esquema JSON, enrutamiento del grafo, selección de 2 respuestas débiles, RBAC, anonimización, estadística del gate.
- **Probabilístico (LLM):** calificaciones del Evaluador, preguntas del Entrevistador, ejemplos mejorados. Siempre detrás de `LLMClient` → se sustituye por `FakeLLM` en pruebas.

## Contrato `LLMClient`
`complete(task, system, user, json_mode, payload) -> str`. `task` ∈ `interviewer.first|next|followup`, `evaluator.evaluate|improve`.

## Datos (RIF-01..05) — `backend/app/db/models.py`
`users`, `interview_sessions`, `message_turns`, `model_evaluations`, `user_feedback`, `golden_dataset`, `rubrics`, `study_resources`. Sin migraciones aún (T-107).

## API actual — `backend/app/api/`
| Método y ruta | RF | Estado |
|---|---|---|
| POST `/api/sessions` | RF-01/02 | ✅ (store en memoria) |
| POST `/api/sessions/{id}/answer` | RF-03 | ✅ |
| GET `/api/sessions/{id}/metrics` | RF-04 | ✅ |
| GET `/api/sessions/{id}/report` | RF-05 | ✅ (sin catálogo real ni PDF backend) |
| POST `/api/sessions/{id}/feedback` | RF-06 | ✅ (en memoria) |
| `/api/students/me/history`, `/rubrics`, `/golden`, `/hitl/queue`, `/admin/*` | RF-07..13 | 501 con puntero a la tarea |
