"""Agente Entrevistador. Genera primera pregunta, siguiente tema o seguimiento (RN-03/RN-05)."""
from app.agents import prompts
from app.agents.state import InterviewState, history_summary
from app.core.constants import DEEPEN_DIMENSIONS
from app.services.llm_client import LLMClient


def _weakest_deepen_dimension(evaluation: dict) -> str:
    return min(DEEPEN_DIMENSIONS, key=lambda d: evaluation[d])


def generate_question(llm: LLMClient, state: InterviewState, mode: str) -> str:
    """mode: 'first' | 'next' | 'followup'."""
    extra, payload = "", {"topic_index": state.get("topic_index", 0)}
    if mode == "followup":
        weak = _weakest_deepen_dimension(state["evaluation"])
        payload["weak_dimension"] = weak
        extra = f"Profundiza en la dimension '{weak}' de la respuesta anterior."
    system = prompts.INTERVIEWER_SYSTEM.format(
        target_role=state.get("target_role", ""), seniority=state.get("seniority", ""))
    user = prompts.INTERVIEWER_USER.format(
        cv_text=state.get("cv_text", "")[:2000], job_description=state.get("job_description", "")[:1500],
        history=history_summary(state), mode=mode, extra=extra)
    return llm.complete(f"interviewer.{mode}", system, user, payload=payload).strip()
