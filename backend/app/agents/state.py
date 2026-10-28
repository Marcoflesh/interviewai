"""Estado compartido del grafo LangGraph (RF-03). Un invoke del grafo = un turno."""
from typing import TypedDict


class InterviewState(TypedDict, total=False):
    session_id: str
    target_role: str
    seniority: str
    cv_text: str               # YA anonimizado (RN-10)
    job_description: str
    max_turns: int             # 5..10 (RN-01). Los follow-ups CUENTAN como respuestas (D-02)
    answered_count: int
    topic_index: int
    in_followup: bool
    current_question: str
    current_answer: str        # vacio => aun no hay respuesta que evaluar
    features: dict             # AnswerFeatures.to_dict() (RN-04)
    evaluation: dict           # EvaluationResult.model_dump() del ultimo turno
    status: str                # SessionStatus.value
    history: list[dict]        # [{question, answer, features, evaluation, is_followup}]


def history_summary(state: InterviewState, last: int = 4) -> str:
    """Resumen corto del historial para el prompt (RF-03 paso 3)."""
    rows = []
    for h in state.get("history", [])[-last:]:
        ev = h["evaluation"]
        rows.append(f"- P: {h['question'][:80]} | S{ev['situacion']} T{ev['tarea']} A{ev['accion']} R{ev['resultado']}")
    return "\n".join(rows) or "(sin historial)"
