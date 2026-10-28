# Trazabilidad SRS → código
Estado: ✅ implementado y probado · 🟡 parcial/esqueleto · ⬜ pendiente

| Req. | Estado | Dónde | Pruebas / nota |
|---|---|---|---|
| RF-01 carga CV+oferta | 🟡 | `api/sessions.py::start_session`, `index.html` | Texto plano; falta subir archivo (T-407) |
| RF-02 iniciar sesión | ✅ | `api/sessions.py`, `agents/graph.py` | `test_api` |
| RF-03 evaluar y decidir estado | ✅ | `agents/graph.py`, `evaluator.py` | `test_graph` (con FakeLLM) |
| RF-04 panel métricas | ✅ | `frontend/js/chat.js`, `css/metrics.css` | Sin prueba en navegador |
| RF-05 reporte final | 🟡 | `services/report.py`, `report.html` | Falta catálogo real, PDF backend (T-401/402) |
| RF-06 CSAT | 🟡 | `api/sessions.py::feedback` | En memoria (T-404) |
| RF-07 historial / evolución | ⬜ | `api/stubs.py` | T-405 |
| RF-08 rúbricas y recursos | ⬜ | modelos `rubrics`, `study_resources` | T-601 |
| RF-09 Golden Dataset | ⬜ | modelo `golden_dataset` | T-501 |
| RF-10 Human-in-the-loop | ⬜ | `api/stubs.py` | T-503 |
| RF-11 config. grafo/prompts | 🟡 | `agents/prompts.py` | Sin UI/versionado (T-302) |
| RF-12 validación y sesgos | 🟡 | `mlops/evaluate_golden.py`, `services/stats.py` | Falta auditoría de sesgos (T-504) |
| RF-13 tablero analítico | ⬜ | `api/stubs.py` | T-602 |
| RF-14 pipelines / anonimización | 🟡 | `services/anonymizer.py` | Regex; falta NER y pipeline (T-106/T-603) |
| RF-15 Docker versionado | 🟡 | `docker-compose.yml`, `Dockerfile`s | **Nunca construido** (T-001) |
| RN-01 5–10 respuestas | ✅ | `schemas/api.py`, `graph.py` | `test_graph` |
| RN-02 vector 1–5 | ✅ | `schemas/evaluation.py` | `test_schema` |
| RN-03 profundizar | ✅ | `graph.py::route_after_eval` | `test_graph` |
| RN-04 Regex/longitud | ✅ | `services/features.py` | `test_features` |
| RN-05 avance/cierre | ✅ | `graph.py` | `test_graph` |
| RN-06 2 débiles + plan | ✅/🟡 | `services/report.py` | Plan con catálogo vacío |
| RN-07 gate 0.75 | ✅ | `services/stats.py`, `mlops/` | Falta Golden Dataset real |
| RN-08 sin sesgo | ⬜ | prompt con cláusula | T-304, T-504 |
| RN-09 CSAT / JSON <0.5% | 🟡 | `core/monitor.py` | Monitor en memoria (T-702) |
| RN-10 anonimización | 🟡 | `services/anonymizer.py` | Ver D-12 |
| RN-11 revisión mensual | ⬜ | — | T-704 |
| RN-12 Docker/Python fijo | 🟡 | `Dockerfile`, `requirements.txt` | Ver RF-15 |
| RNF-01 < 2.5 s/turno | ⬜ | se mide `latency_ms` | Solo FakeLLM; T-303 |
| RNF-02 reporte < 8 s | ⬜ | — | T-402 |
| RNF-03 correlación 0.75 | 🟡 | ver RN-07 | |
| RNF-05 JSON <0.5% | 🟡 | `evaluator.py` (1 reintento) | |
| RNF-06 CSS/CSAT>80% | 🟡 | `frontend/css/` | |
| RNF-07 RBAC | 🟡 | `core/rbac.py`, `api/deps.py` | Auth real pendiente (T-114) |
| RNF-08 LangGraph/Colab | 🟡 | `agents/graph.py`, `mlops/` | |
| RIN-01 LLM por API | 🟡 | `services/llm_client.py` | Stubs Gemini/OpenAI (T-301) |
| RIN-02 PostgreSQL | 🟡 | `db/models.py` | Sin conexión real (T-107/T-108) |
| RIN-03 Colab | 🟡 | `mlops/evaluate_golden.py` | T-505 |
| RIN-04 red Docker | 🟡 | `docker-compose.yml` | Ver RF-15 |
