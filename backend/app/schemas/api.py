"""Contratos HTTP (request/response). El frontend (frontend/js/api.js) depende de estos nombres."""
from pydantic import BaseModel, Field

from app.core.constants import MAX_QUESTIONS, MIN_QUESTIONS


class StartSessionRequest(BaseModel):  # RF-01 + RF-02
    target_role: str = Field(min_length=2)
    seniority: str = "junior"
    cv_text: str = Field(min_length=20)
    job_description: str = Field(min_length=20)
    career: str | None = None
    university: str | None = None
    model: str | None = None            # modelo de Ollama elegido en la UI ('fake' = demo)
    num_questions: int = Field(default=5, ge=MIN_QUESTIONS, le=MAX_QUESTIONS)


class StartSessionResponse(BaseModel):
    session_id: str
    question: str
    total_questions: int
    anonymization: dict[str, int]


class AnswerRequest(BaseModel):  # RF-03
    answer: str = Field(min_length=1)


class AnswerResponse(BaseModel):
    evaluation: dict
    status: str
    next_question: str | None
    answered_count: int
    total_questions: int
    latency_ms: int
    report_ready: bool


class FeedbackRequest(BaseModel):  # RF-06
    csat: int = Field(ge=1, le=5)
    comment: str | None = None
