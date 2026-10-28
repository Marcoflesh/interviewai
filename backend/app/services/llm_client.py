"""Cliente LLM abstracto (RIN-01). Un solo punto de integracion con Gemini / OpenAI.

- `FakeLLM`: determinista, sin red ni API keys. Sirve para desarrollo offline,
  pruebas y demo. NO es un modelo real: sus calificaciones salen de heuristicas.
- `GeminiLLM` / `OpenAILLM`: STUBS. TODO (ROADMAP T-301): implementar llamadas
  reales con salida JSON estructurada y medir latencia (RNF-01 < 2.5 s/turno).

`task` identifica la llamada (para logging, enrutar prompts y para FakeLLM):
  interviewer.first | interviewer.next | interviewer.followup |
  evaluator.evaluate | evaluator.improve
`payload` lleva datos estructurados; los proveedores reales pueden ignorarlo.
"""
import json
from typing import Protocol

from app.config import settings

_QUESTION_BANK = [
    "Cuentame de un proyecto academico o personal del que te sientas orgulloso. Que problema resolvias?",
    "Describe una situacion en la que tuviste un conflicto en un equipo. Como lo manejaste?",
    "Platicame de una ocasion en la que tuviste que aprender una tecnologia nueva muy rapido.",
    "Cuentame de un error que cometiste en un proyecto y que hiciste para corregirlo.",
    "Describe un momento en el que lideraste una iniciativa sin tener autoridad formal.",
    "Cuentame de una vez que trabajaste bajo mucha presion o con una fecha limite muy ajustada.",
    "Describe un caso en el que mejoraste un proceso o un sistema existente.",
    "Platicame de una decision tecnica dificil que tomaste y como la justificaste.",
    "Cuentame de una retroalimentacion dificil que recibiste y que hiciste con ella.",
    "Por que te interesa esta vacante y como encaja tu experiencia con ella?",
]


class LLMClient(Protocol):
    def complete(self, task: str, system: str, user: str, json_mode: bool = False,
                 payload: dict | None = None) -> str: ...


class FakeLLM:
    """LLM falso determinista. Heuristicas: ver `_fake_scores`."""

    def complete(self, task, system, user, json_mode=False, payload=None) -> str:
        payload = payload or {}
        if task == "interviewer.first":
            return _QUESTION_BANK[0]
        if task == "interviewer.next":
            return _QUESTION_BANK[payload.get("topic_index", 1) % len(_QUESTION_BANK)]
        if task == "interviewer.followup":
            dim = payload.get("weak_dimension", "resultado")
            if dim == "resultado":
                return "Puedes cuantificar el resultado? Por ejemplo, en porcentaje, tiempo ahorrado o personas beneficiadas."
            return "Que hiciste TU de forma concreta? Describe tus acciones paso a paso."
        if task == "evaluator.evaluate":
            return json.dumps(_fake_scores(payload.get("features", {})))
        if task == "evaluator.improve":
            return json.dumps({
                "ejemplo_mejorado": (
                    "Situacion: en mi proyecto de ... Tarea: me toco ... Accion: yo disene, implemente y probe ... "
                    "Resultado: reduje el tiempo en 30% y beneficie a 120 usuarios."
                ),
            })
        raise ValueError(f"task desconocida: {task}")


def _fake_scores(features: dict) -> dict:
    words = features.get("length_words", 0)
    metrics = features.get("metric_count", 0)
    return {
        "situacion": 3 if words >= 25 else 2,
        "tarea": 3 if words >= 25 else 2,
        "accion": 4 if words >= 60 else (3 if words >= 40 else 2),
        "resultado": 4 if (metrics >= 1 and words >= 30) else 2,
        "claridad_tecnica": 3,
        "pertinencia": 3,
        "fortalezas": ["Respuesta con estructura reconocible"] if words >= 40 else [],
        "areas_mejora": [] if metrics else ["Agrega metricas cuantitativas al Resultado"],
    }


class GeminiLLM:  # pragma: no cover - stub
    def __init__(self, api_key: str, model: str):
        self.api_key, self.model = api_key, model

    def complete(self, task, system, user, json_mode=False, payload=None) -> str:
        raise NotImplementedError("TODO T-301: implementar llamada a Gemini (salida JSON estructurada)")


class OpenAILLM:  # pragma: no cover - stub
    def __init__(self, api_key: str, model: str):
        self.api_key, self.model = api_key, model

    def complete(self, task, system, user, json_mode=False, payload=None) -> str:
        raise NotImplementedError("TODO T-301: implementar llamada a OpenAI (response_format json)")


def get_llm() -> LLMClient:
    if settings.llm_provider == "gemini":
        return GeminiLLM(settings.gemini_api_key, settings.llm_model)
    if settings.llm_provider == "openai":
        return OpenAILLM(settings.openai_api_key, settings.llm_model)
    return FakeLLM()
