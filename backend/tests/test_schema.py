import json
import pytest
from app.schemas.evaluation import EvaluationFormatError, parse_evaluation

OK = {"situacion": 3, "tarea": 3, "accion": 4, "resultado": 2, "claridad_tecnica": 3, "pertinencia": 3}


def test_valid_and_fenced():
    assert parse_evaluation(json.dumps(OK)).accion == 4
    assert parse_evaluation("```json\n" + json.dumps(OK) + "\n```").resultado == 2


@pytest.mark.parametrize("raw", ["no es json", json.dumps({**OK, "accion": 6}), json.dumps({**OK, "tarea": 0}),
                                 json.dumps({k: v for k, v in OK.items() if k != "tarea"}), ""])
def test_invalid_raises(raw):
    with pytest.raises(EvaluationFormatError):
        parse_evaluation(raw)
