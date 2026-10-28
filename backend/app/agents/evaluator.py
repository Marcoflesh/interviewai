"""Agente Evaluador (LLM-as-a-Judge). RN-02, RF-03 pasos 4-6, flujo 6A."""
from app.agents import prompts
from app.agents.state import InterviewState, history_summary
from app.core.monitor import format_monitor
from app.schemas.evaluation import EvaluationFormatError, EvaluationResult, parse_evaluation
from app.services.llm_client import LLMClient


def evaluate_answer(llm: LLMClient, state: InterviewState, retries: int = 1) -> EvaluationResult:
    """Califica la respuesta. Reintenta `retries` veces si el JSON es invalido (6A.2).
    Si todos los intentos fallan, lanza EvaluationFormatError (la API muestra el
    mensaje de 6A.3 y NO modifica el estado de la sesion)."""
    feats = state.get("features", {})
    user = prompts.EVALUATOR_USER.format(
        target_role=state.get("target_role", ""), seniority=state.get("seniority", ""),
        history=history_summary(state), question=state["current_question"],
        answer=state["current_answer"], length_words=feats.get("length_words", 0),
        metric_count=feats.get("metric_count", 0),
    )
    last_error: EvaluationFormatError | None = None
    for _ in range(retries + 1):
        raw = llm.complete("evaluator.evaluate", prompts.EVALUATOR_SYSTEM, user,
                           json_mode=True, payload={"features": feats})
        try:
            result = parse_evaluation(raw)
            format_monitor.record(ok=True)
            return result
        except EvaluationFormatError as exc:
            format_monitor.record(ok=False)
            last_error = exc
    raise last_error  # type: ignore[misc]
