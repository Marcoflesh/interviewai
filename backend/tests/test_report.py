from app.services.llm_client import FakeLLM
from app.services.report import build_report, pick_weakest, score_evolution_rate


def turn(n, s, t, a, r, c=3, p=3):
    return {"question": f"q{n}", "answer": f"a{n}", "evaluation": dict(
        situacion=s, tarea=t, accion=a, resultado=r, claridad_tecnica=c, pertinencia=p)}


def test_weakest_two_with_tiebreak():
    turns = [turn(1, 4, 4, 4, 4), turn(2, 2, 2, 2, 2), turn(3, 3, 3, 3, 3), turn(4, 2, 2, 3, 1)]
    weak = pick_weakest(turns)
    assert [w["question"] for w in weak] == ["q2", "q4"] or [w["question"] for w in weak] == ["q4", "q2"]


def test_evolution_rate():
    assert score_evolution_rate(3.3, [3.0]) == (3.3 - 3.0) / 3.0 * 100
    assert score_evolution_rate(3.0, []) is None


def test_build_report_and_fallback():
    turns = [turn(i, 2 + i % 3, 3, 3, 2 + i % 2) for i in range(5)]
    rep = build_report(FakeLLM(), turns=turns, previous_scores=[2.5],
                       resource_catalog=[{"title": "STAR", "url": "http://x", "tags": ["resultado", "accion"]}])
    assert len(rep["weakest_answers"]) == 2 and not rep["examples_pending"]

    class Broken(FakeLLM):
        def complete(self, task, *a, **k):
            if task == "evaluator.improve":
                raise TimeoutError
            return super().complete(task, *a, **k)

    rep = build_report(Broken(), turns=turns, previous_scores=[], resource_catalog=[])
    assert rep["examples_pending"] and rep["session_score"] > 0          # RF-05 6A: degrada, no falla
