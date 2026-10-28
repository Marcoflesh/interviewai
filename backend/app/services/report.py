"""Reporte final y Plan de Accion (RF-05, RN-06). Logica determinista + 1 llamada LLM.

Definiciones (ver DECISIONS.md D-04, D-05):
- Debilidad de una respuesta = promedio de las 6 dimensiones; desempate: menor
  resultado, luego menor accion, luego turno mas temprano.
- Tasa de Evolucion de Puntaje = (puntaje_actual - promedio_previo) / promedio_previo * 100.
  El SRS no la define: CONFIRMAR con el profesor/PO (ROADMAP T-405).
"""
import json

from app.agents import prompts
from app.core.constants import ALL_DIMENSIONS, WEAKEST_ANSWERS_IN_REPORT
from app.services.llm_client import LLMClient


def turn_score(evaluation: dict) -> float:
    return sum(evaluation[d] for d in ALL_DIMENSIONS) / len(ALL_DIMENSIONS)


def pick_weakest(turns: list[dict], n: int = WEAKEST_ANSWERS_IN_REPORT) -> list[dict]:
    indexed = list(enumerate(turns))
    indexed.sort(key=lambda it: (turn_score(it[1]["evaluation"]), it[1]["evaluation"]["resultado"],
                                 it[1]["evaluation"]["accion"], it[0]))
    return [t for _, t in indexed[:n]]


def session_score(turns: list[dict]) -> float:
    return sum(turn_score(t["evaluation"]) for t in turns) / len(turns) if turns else 0.0


def score_evolution_rate(current: float, previous_scores: list[float]) -> float | None:
    if not previous_scores:
        return None
    prev = sum(previous_scores) / len(previous_scores)
    return (current - prev) / prev * 100 if prev else None


def dimension_averages(turns: list[dict]) -> dict[str, float]:
    return {d: sum(t["evaluation"][d] for t in turns) / len(turns) for d in ALL_DIMENSIONS}


def select_resources(averages: dict[str, float], catalog: list[dict], k: int = 3) -> list[dict]:
    """Recursos curados por el PO (RF-08) cuyos `tags` coinciden con las 2 dimensiones mas bajas.
    TODO T-403: que el Agente Evaluador personalice la seleccion."""
    focus = sorted(averages, key=averages.get)[:2]
    return [r for r in catalog if set(r.get("tags", [])) & set(focus)][:k]


def build_report(llm: LLMClient, *, turns: list[dict], previous_scores: list[float],
                 resource_catalog: list[dict]) -> dict:
    score = session_score(turns)
    averages = dimension_averages(turns)
    improvements, pending = [], False
    for t in pick_weakest(turns):
        try:  # RF-05 flujo 6A: si el LLM falla, se entrega el resumen cuantitativo
            raw = llm.complete("evaluator.improve", prompts.IMPROVE_SYSTEM,
                               f"Pregunta: {t['question']}\nRespuesta: {t['answer']}", json_mode=True)
            example = json.loads(raw)["ejemplo_mejorado"]
        except Exception:
            pending, example = True, None
        improvements.append({"question": t["question"], "answer": t["answer"],
                             "evaluation": t["evaluation"], "ejemplo_mejorado": example})
    return {
        "session_score": round(score, 2),
        "score_evolution_rate": score_evolution_rate(score, previous_scores),
        "dimension_averages": {k: round(v, 2) for k, v in averages.items()},
        "weakest_answers": improvements,
        "action_plan": {"focus_dimensions": sorted(averages, key=averages.get)[:2],
                        "resources": select_resources(averages, resource_catalog)},
        "examples_pending": pending,
    }
