"""Grafo de estados LangGraph (RF-03, RN-03, RN-05, RN-12/RNF-08).

Un `graph.invoke(state)` procesa UN turno:

  START --(sin respuesta)--> generar_primera_pregunta --> END
  START --(con respuesta)--> extraer_features --> evaluar_respuesta --(arista condicional)-->
        profundizar_pregunta | pasar_a_siguiente_tema | finalizar_entrevista --> END

Arista condicional (`route_after_eval`), en orden de prioridad:
  1. answered_count >= max_turns            -> finalizar_entrevista   (RF-03 9A)
  2. Accion<3 o Resultado<3 y NO en followup -> profundizar_pregunta  (RN-03)
  3. en otro caso                           -> pasar_a_siguiente_tema (RN-05)
Decisiones de ambiguedad: docs/DECISIONS.md D-01, D-02.
La generacion del reporte (RF-05) NO esta en el grafo: la invoca la capa de servicio
al ver status == finalizar_entrevista (punto de extension del SRS).
"""
from langgraph.graph import END, START, StateGraph

from app.agents.evaluator import evaluate_answer
from app.agents.interviewer import generate_question
from app.agents.state import InterviewState
from app.config import settings
from app.core.constants import DEEPEN_DIMENSIONS, WEAK_THRESHOLD, SessionStatus
from app.services.features import extract_features
from app.services.llm_client import LLMClient

N_FIRST = "generar_primera_pregunta"
N_FEATURES = "extraer_features"
N_EVAL = "evaluar_respuesta"
N_DEEPEN = SessionStatus.PROFUNDIZAR.value
N_NEXT = SessionStatus.SIGUIENTE.value
N_END = SessionStatus.FINALIZADA.value


def route_entry(state: InterviewState) -> str:
    return N_FEATURES if state.get("current_answer") else N_FIRST


def route_after_eval(state: InterviewState) -> str:
    """Logica PURA y determinista (la parte probabilistica esta en el Evaluador)."""
    if state["answered_count"] >= state["max_turns"]:
        return N_END
    ev = state["evaluation"]
    weak = any(ev[d] < WEAK_THRESHOLD for d in DEEPEN_DIMENSIONS)
    if weak and not state.get("in_followup", False):
        return N_DEEPEN
    return N_NEXT


def build_graph(llm: LLMClient):
    def generar_primera_pregunta(state: InterviewState) -> dict:
        q = generate_question(llm, state, "first")
        return {"current_question": q, "current_answer": "", "topic_index": 0,
                "answered_count": 0, "in_followup": False, "history": [],
                "status": SessionStatus.INICIADA.value}

    def extraer_features(state: InterviewState) -> dict:  # RN-04
        return {"features": extract_features(state["current_answer"]).to_dict()}

    def evaluar_respuesta(state: InterviewState) -> dict:  # RN-02
        result = evaluate_answer(llm, state, retries=settings.json_retry_attempts)
        ev = result.model_dump()
        entry = {"question": state["current_question"], "answer": state["current_answer"],
                 "features": state["features"], "evaluation": ev,
                 "is_followup": state.get("in_followup", False)}
        return {"evaluation": ev, "history": state.get("history", []) + [entry],
                "answered_count": state.get("answered_count", 0) + 1}

    def profundizar_pregunta(state: InterviewState) -> dict:  # RN-03
        q = generate_question(llm, state, "followup")
        return {"current_question": q, "current_answer": "", "in_followup": True,
                "status": SessionStatus.PROFUNDIZAR.value}

    def pasar_a_siguiente_tema(state: InterviewState) -> dict:  # RN-05
        nxt = state.get("topic_index", 0) + 1
        q = generate_question(llm, {**state, "topic_index": nxt}, "next")
        return {"current_question": q, "current_answer": "", "in_followup": False,
                "topic_index": nxt, "status": SessionStatus.SIGUIENTE.value}

    def finalizar_entrevista(state: InterviewState) -> dict:  # nodo terminal
        return {"current_question": "", "current_answer": "", "status": SessionStatus.FINALIZADA.value}

    g = StateGraph(InterviewState)
    g.add_node(N_FIRST, generar_primera_pregunta)
    g.add_node(N_FEATURES, extraer_features)
    g.add_node(N_EVAL, evaluar_respuesta)
    g.add_node(N_DEEPEN, profundizar_pregunta)
    g.add_node(N_NEXT, pasar_a_siguiente_tema)
    g.add_node(N_END, finalizar_entrevista)
    g.add_conditional_edges(START, route_entry, {N_FEATURES: N_FEATURES, N_FIRST: N_FIRST})
    g.add_edge(N_FEATURES, N_EVAL)
    g.add_conditional_edges(N_EVAL, route_after_eval, {N_DEEPEN: N_DEEPEN, N_NEXT: N_NEXT, N_END: N_END})
    for n in (N_FIRST, N_DEEPEN, N_NEXT, N_END):
        g.add_edge(n, END)
    return g.compile()
