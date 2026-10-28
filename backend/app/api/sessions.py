"""Endpoints del estudiante: RF-01..RF-07. Funcionales con FakeLLM + store en memoria."""
import time

from fastapi import APIRouter, Depends, HTTPException

from app.agents.graph import build_graph
from app.core.constants import TURN_LATENCY_BUDGET_S, SessionStatus
from app.core.rbac import Permission
from app.api.deps import require
from app.schemas.api import (AnswerRequest, AnswerResponse, FeedbackRequest,
                             StartSessionRequest, StartSessionResponse)
from app.schemas.evaluation import EvaluationFormatError
from app.services.anonymizer import anonymize
from app.services.llm_client import LLMUnavailableError, get_llm
from app.services.report import build_report
from app.services.session_store import store

router = APIRouter(prefix="/api/sessions", tags=["estudiante"])


def _graph_and_llm(model: str | None):
    llm = get_llm(model)           # un grafo por solicitud: barato y permite modelo por sesion
    return build_graph(llm), llm

FORMAT_ERROR_MSG = "No fue posible procesar la evaluacion, intenta enviar tu respuesta nuevamente"  # RF-03 6A.3


def _get(session_id: str) -> dict:
    state = store.get(session_id)
    if state is None:
        raise HTTPException(404, "Sesion no encontrada")
    return state


@router.post("", response_model=StartSessionResponse, dependencies=[Depends(require(Permission.RUN_SESSION))])
def start_session(body: StartSessionRequest):
    cv = anonymize(body.cv_text)                      # RN-10: ANTES de guardar
    state = {"target_role": body.target_role, "seniority": body.seniority, "cv_text": cv.text,
             "job_description": body.job_description, "max_turns": body.num_questions}
    state["llm_model"] = body.model
    graph, _ = _graph_and_llm(body.model)
    try:
        state = graph.invoke(state)                   # primera pregunta
    except LLMUnavailableError as exc:
        raise HTTPException(503, str(exc)) from None
    sid = store.create(state)
    return StartSessionResponse(session_id=sid, question=state["current_question"],
                                total_questions=body.num_questions, anonymization=cv.counts)


@router.post("/{session_id}/answer", response_model=AnswerResponse,
             dependencies=[Depends(require(Permission.RUN_SESSION))])
def answer(session_id: str, body: AnswerRequest):
    state = _get(session_id)
    if state["status"] == SessionStatus.FINALIZADA.value:
        raise HTTPException(409, "La entrevista ya finalizo")
    t0 = time.perf_counter()
    graph, _ = _graph_and_llm(state.get("llm_model"))
    try:
        new_state = graph.invoke({**state, "current_answer": body.answer})
    except LLMUnavailableError as exc:
        raise HTTPException(503, str(exc)) from None
    except EvaluationFormatError:                     # 6A.3: se conserva el estado previo
        raise HTTPException(502, FORMAT_ERROR_MSG) from None
    latency_ms = int((time.perf_counter() - t0) * 1000)
    # TODO T-205: registrar si latency_ms/1000 > TURN_LATENCY_BUDGET_S (RNF-01)
    store.save(session_id, new_state)
    done = new_state["status"] == SessionStatus.FINALIZADA.value
    return AnswerResponse(evaluation=new_state["evaluation"], status=new_state["status"],
                          next_question=new_state["current_question"] or None,
                          answered_count=new_state["answered_count"], total_questions=new_state["max_turns"],
                          latency_ms=latency_ms, report_ready=done)


@router.get("/{session_id}/metrics", dependencies=[Depends(require(Permission.VIEW_LIVE_METRICS))])
def metrics(session_id: str):  # RF-04
    state = _get(session_id)
    return {"turns": [h["evaluation"] for h in state.get("history", [])], "status": state["status"]}


@router.get("/{session_id}/report", dependencies=[Depends(require(Permission.DOWNLOAD_REPORT))])
def report(session_id: str):  # RF-05
    state = _get(session_id)
    if state["status"] != SessionStatus.FINALIZADA.value:
        raise HTTPException(409, "El reporte solo existe al finalizar la entrevista")
    if "report" not in state:
        # TODO T-401: catalogo real (RF-08) y puntajes previos del estudiante (RF-07)
        state["report"] = build_report(_graph_and_llm(state.get("llm_model"))[1], turns=state["history"], previous_scores=[], resource_catalog=[])
        store.save(session_id, state)
    return state["report"]
    # TODO T-402: endpoint de PDF (GET /report.pdf) < 8 s (RNF-02)


@router.post("/{session_id}/feedback", dependencies=[Depends(require(Permission.SUBMIT_CSAT))])
def feedback(session_id: str, body: FeedbackRequest):  # RF-06
    _get(session_id)
    store.feedback.setdefault(session_id, []).append(body.model_dump())  # TODO T-404: tabla user_feedback
    return {"ok": True}
