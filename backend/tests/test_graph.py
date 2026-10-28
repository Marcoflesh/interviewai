"""RN-03 / RN-05 / RF-03: enrutamiento del grafo y flujo completo con FakeLLM."""
import json
import pytest
from app.agents.graph import build_graph, route_after_eval
from app.core.constants import SessionStatus
from app.schemas.evaluation import EvaluationFormatError
from app.services.llm_client import FakeLLM

STRONG = ("Durante mi servicio social lidere la migracion de un sistema de inventario a la nube; "
          "yo disene el esquema, escribi los scripts y capacite a 12 personas, logrando reducir 40% el tiempo de captura.") * 2
WEAK = "Pues hice lo que me pidieron y salio bien."


def ev(a, r):
    return {"situacion": 3, "tarea": 3, "accion": a, "resultado": r, "claridad_tecnica": 3, "pertinencia": 3}


@pytest.mark.parametrize("a,r,followup,answered,expected", [
    (2, 4, False, 1, "profundizar_pregunta"),
    (4, 2, False, 1, "profundizar_pregunta"),
    (3, 3, False, 1, "pasar_a_siguiente_tema"),      # 3 NO es menor a 3
    (2, 2, True, 2, "pasar_a_siguiente_tema"),       # RN-05: tras el seguimiento se avanza
    (5, 5, False, 5, "finalizar_entrevista"),        # ultimo turno
    (1, 1, False, 5, "finalizar_entrevista"),        # ultimo turno gana aunque sea debil (D-01)
])
def test_route_after_eval(a, r, followup, answered, expected):
    state = {"evaluation": ev(a, r), "in_followup": followup, "answered_count": answered, "max_turns": 5}
    assert route_after_eval(state) == expected


def test_full_interview_weak_then_strong():
    g = build_graph(FakeLLM())
    s = g.invoke({"target_role": "Dev", "seniority": "junior", "cv_text": "cv", "job_description": "jd", "max_turns": 5})
    assert s["status"] == "iniciada" and s["current_question"]
    s = g.invoke({**s, "current_answer": WEAK})
    assert s["status"] == SessionStatus.PROFUNDIZAR.value and s["in_followup"]
    s = g.invoke({**s, "current_answer": WEAK})                      # responde el seguimiento
    assert s["status"] == SessionStatus.SIGUIENTE.value and not s["in_followup"]
    while s["status"] != SessionStatus.FINALIZADA.value:
        s = g.invoke({**s, "current_answer": STRONG})
    assert s["answered_count"] == 5 and len(s["history"]) == 5 and s["current_question"] == ""


class BadJsonLLM(FakeLLM):
    def complete(self, task, *a, **k):
        return "basura" if task == "evaluator.evaluate" else super().complete(task, *a, **k)


def test_bad_json_raises_after_retry_and_keeps_state():
    g = build_graph(BadJsonLLM())
    s = g.invoke({"target_role": "Dev", "seniority": "junior", "cv_text": "", "job_description": "", "max_turns": 5})
    with pytest.raises(EvaluationFormatError):
        g.invoke({**s, "current_answer": STRONG})
    assert s["answered_count"] == 0                                   # el estado previo no se altero
