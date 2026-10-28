"""Validacion pre-despliegue contra el Golden Dataset (RN-07, RF-12, RIN-03). Compatible con Google Colab.

Uso local:   cd backend && python ../mlops/evaluate_golden.py ../mlops/golden_dataset/sample_PLACEHOLDER.csv
Colab:       clonar repo, `pip install -r backend/requirements.txt`, ejecutar este archivo.
Con LLM_PROVIDER=fake solo valida la tuberia (las notas del FakeLLM NO son un modelo real).

TODO (ROADMAP T-504): auditoria de sesgos RN-08 -> `invariance_audit` (swap de genero/nacionalidad/modismos
en la respuesta y verificar que el puntaje no cambie); correlacion por dimension y por area; guardar
resultados en `golden_dataset.model_scores`.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.schemas.evaluation import parse_evaluation          # noqa: E402
from app.services.features import extract_features           # noqa: E402
from app.services.llm_client import get_llm                  # noqa: E402
from app.services.stats import passes_golden_gate            # noqa: E402


def model_score(llm, question: str, answer: str) -> float:
    feats = extract_features(answer).to_dict()
    raw = llm.complete("evaluator.evaluate", "", f"{question}\n{answer}", json_mode=True, payload={"features": feats})
    return parse_evaluation(raw).mean_score


def invariance_audit(*_a, **_k):  # pragma: no cover
    raise NotImplementedError("TODO T-504: auditoria de sesgos (RN-08 / RNF-04)")


def main(path: str) -> int:
    llm = get_llm()
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    human = [float(r["human_mean"]) for r in rows]
    model = [model_score(llm, r["question"], r["answer"]) for r in rows]
    result = passes_golden_gate(human, model)
    print(result)
    return 0 if result["approved"] else 1       # codigo != 0 => bloquear despliegue (CI)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
