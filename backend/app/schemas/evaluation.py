"""Esquema JSON de la salida del Agente Evaluador (RN-02, RIF-03, RF-03 paso 6).

Cualquier salida del LLM que no cumpla este esquema cuenta como error de formato
(RNF-05, < 0.5%) y dispara el flujo alterno 6A (un reintento y luego mensaje).
"""
import json
import re

from pydantic import BaseModel, Field, ValidationError, field_validator

from app.core.constants import ALL_DIMENSIONS, SCORE_MAX, SCORE_MIN, STAR_DIMENSIONS


class EvaluationFormatError(ValueError):
    """La salida del LLM no es JSON valido o no cumple el esquema."""


class EvaluationResult(BaseModel):
    situacion: int = Field(ge=SCORE_MIN, le=SCORE_MAX)
    tarea: int = Field(ge=SCORE_MIN, le=SCORE_MAX)
    accion: int = Field(ge=SCORE_MIN, le=SCORE_MAX)
    resultado: int = Field(ge=SCORE_MIN, le=SCORE_MAX)
    claridad_tecnica: int = Field(ge=SCORE_MIN, le=SCORE_MAX)
    pertinencia: int = Field(ge=SCORE_MIN, le=SCORE_MAX)
    fortalezas: list[str] = Field(default_factory=list)
    areas_mejora: list[str] = Field(default_factory=list)

    @field_validator("fortalezas", "areas_mejora", mode="before")
    @classmethod
    def _none_to_list(cls, v):
        return [] if v is None else v

    @property
    def mean_score(self) -> float:
        return sum(getattr(self, d) for d in ALL_DIMENSIONS) / len(ALL_DIMENSIONS)

    @property
    def star_mean(self) -> float:
        return sum(getattr(self, d) for d in STAR_DIMENSIONS) / len(STAR_DIMENSIONS)


_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def parse_evaluation(raw: str) -> EvaluationResult:
    """Valida la salida cruda del LLM. Tolera cercas ```json ... ```."""
    cleaned = _FENCE_RE.sub("", (raw or "").strip())
    try:
        return EvaluationResult.model_validate(json.loads(cleaned))
    except (json.JSONDecodeError, ValidationError, TypeError) as exc:
        raise EvaluationFormatError(str(exc)) from exc
