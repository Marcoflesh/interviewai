# Roadmap de implementación

Leyenda: ✅ hecho · 🔄 en curso · ⬜ pendiente. Prioridad (P1 alta … P3 baja) sale de la tabla de priorización del SRS (RF-03, RF-05, RF-11, RF-12 = riesgo alto → se atacan temprano).
Cada tarea debe terminar con pruebas en verde y la documentación actualizada (ver `AGENTS.md`).

## Fase 0 — Fundaciones (RF-15, RN-12)
| ID | Tarea | Estado | Criterio de aceptación |
|---|---|---|---|
| T-001 | Validar `docker compose up --build` (nunca se ha construido) y ajustar Dockerfiles/CORS | ⬜ P1 | Frontend en :8080 completa una entrevista contra backend en :8000 |
| T-002 | CI (GitHub Actions): `pytest` + `evaluate_golden.py` como gate | ⬜ P2 | PR falla si pytest o gate fallan |
| T-003 | Inicializar git, ramas, convención de commits | ⬜ P3 | Repo con historial limpio |

## Fase 1 — Datos y seguridad (RF-14, RN-10, RNF-07)
| ID | Tarea | Estado | Criterio |
|---|---|---|---|
| T-101…T-105 | Constantes, features Regex, esquema JSON, RBAC (modelo), anonimizador v0 | ✅ | 31 pruebas en verde |
| T-106 | Anonimizador con NER (nombres, escuelas, empresas) + anonimizar también respuestas del chat (D-12) | ⬜ P2 | Recall ≥ 95 % en 20 CVs de prueba |
| T-107 | Migraciones Alembic para `db/models.py` | ⬜ P1 | `alembic upgrade head` crea el esquema en Postgres |
| T-108 | `PostgresSessionStore` que cumpla `SessionStore`; persistir en `message_turns` y `model_evaluations` | ⬜ P1 | Las pruebas de API pasan con Postgres (testcontainer o compose) |
| T-114 | Autenticación real (JWT/SSO) y quitar stub `X-Role` | ⬜ P2 | Roles verificados desde token; `AUTH_MODE=dev` solo en local |

## Fase 2 — Grafo y agentes (RF-03, RF-11, RN-03/05)
| ID | Tarea | Estado | Criterio |
|---|---|---|---|
| T-201…T-204 | Grafo LangGraph, Evaluador, Entrevistador, reintento 6A | ✅ | `test_graph` |
| T-205 | Medir/alertar latencia por turno (RNF-01) y afinar Regex (números no métricos, cantidades en palabras) | ⬜ P2 | `latency_ms` registrado; casos nuevos en `test_features` |
| T-206 | Usar checkpointer/estado persistente de LangGraph o rehidratar desde BD | ⬜ P2 | Reiniciar backend no pierde sesiones |

## Fase 3 — LLM real (RIN-01, RF-11, RN-08)
| ID | Tarea | Estado | Criterio |
|---|---|---|---|
| T-301 | LLM real: `OllamaLLM` hecho (🔄 falta probar con Ollama real); `GeminiLLM`/`OpenAILLM` siguen como stubs | 🔄 P1 | Evaluación real que cumpla el esquema; tasa de error JSON medida |
| T-302 | Prompts versionados + few-shot por rúbrica; endpoint admin (RF-11) | ⬜ P2 | `prompt_version` guardado en cada evaluación |
| T-303 | Optimizar para < 2.5 s/turno (modelo rápido, prompts cortos, resumen de historial) | ⬜ P1 | p95 < 2.5 s en 50 turnos |
| T-304 | Cláusulas de equidad en prompts (invarianza a género, edad, nacionalidad, modismos) | ⬜ P2 | Pasa auditoría T-504 |

## Fase 4 — Experiencia del estudiante (RF-01, 02, 04, 05, 06, 07)
| ID | Tarea | Estado | Criterio |
|---|---|---|---|
| T-401 | Reporte con catálogo real de recursos y puntajes previos | ⬜ P1 | `build_report` usa BD, no listas vacías |
| T-402 | PDF desde backend (< 8 s, RNF-02) | ⬜ P1 | Descarga PDF limpio; medición de tiempo |
| T-403 | Que el Evaluador personalice la selección de recursos | ⬜ P3 | Recursos coherentes con dimensiones débiles |
| T-404 | CSAT persistente en `user_feedback` + motivo de abandono | ⬜ P2 | Fila creada por sesión |
| T-405 | Historial de sesiones + Tasa de Evolución (**confirmar fórmula D-05**) | ⬜ P2 | `/api/students/me/history` real |
| T-406 | Abandono: marcar `abandonada` si <5 respuestas (RF-05 flujo 1A) | ⬜ P2 | Sin reporte; evento registrado |
| T-407 | Pulir frontend: subir archivo de CV, accesibilidad, pruebas manuales en móvil | ⬜ P2 | Revisión en 375 px y teclado |

## Fase 5 — Validación estadística (RF-09, 10, 12, RN-07/08)
| ID | Tarea | Estado | Criterio |
|---|---|---|---|
| T-501 | Construir Golden Dataset real (50–100 resp., estratificado por carrera) con expertos | ⬜ P1 | CSV/BD con calificaciones humanas |
| T-502 | Cargar CSV a `golden_dataset` y guardar `model_scores` | ⬜ P2 | Script reproducible |
| T-503 | Cola Human-in-the-loop (priorizar pares dudosos) | ⬜ P3 | UI/API para etiquetar |
| T-504 | Auditoría de sesgos (swap de atributos) + correlación por dimensión y área | ⬜ P1 | Reporte con 0 % sesgo detectable o hallazgos |
| T-505 | Notebook de Colab que llame `mlops/evaluate_golden.py` (RIN-03) | ⬜ P3 | Corre de punta a punta en Colab |
| T-506 | Gate RN-07 en CI antes de desplegar (≥ 0.75) | ⬜ P1 | Despliegue bloqueado si falla |

## Fase 6 — Paneles de otros roles (RF-08, 13, 14)
| ID | Tarea | Estado | Criterio |
|---|---|---|---|
| T-601 | CRUD de rúbricas y recursos + vista PO (`po.html`) | ⬜ P2 | PO actualiza catálogo sin tocar código |
| T-602 | Tablero analista (CSAT, evolución, abandono; filtros carrera/universidad/rol) | ⬜ P3 | KPIs desde BD |
| T-603 | Pipelines de banco de preguntas y anonimización masiva | ⬜ P3 | Job reproducible |
| T-604 | Vista admin MLOps (`admin.html`) | ⬜ P3 | Ver prompts, versiones y resultados de auditorías |

## Fase 7 — Endurecimiento
| ID | Tarea | Estado | Criterio |
|---|---|---|---|
| T-701 | Pruebas de carga y latencia | ⬜ P2 | Reporte de p50/p95 |
| T-702 | Exportar tasa de errores JSON (< 0.5 %) a métrica/alerta | ⬜ P2 | Alerta configurada |
| T-703 | Seguridad: CORS estricto, rate limit, secretos, cabeceras | ⬜ P2 | Checklist OWASP básico |
| T-704 | Despliegue y ritual mensual de revisión de prompts (RN-11) | ⬜ P3 | Runbook documentado |

## Orden recomendado
`T-001 → T-107/T-108 → T-301 → T-303 → T-401/T-402 → T-501 → T-504/T-506` y el resto en paralelo según disponibilidad. Camino crítico para la demo: T-001 y T-301.
