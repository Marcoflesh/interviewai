"""Caracteristicas tabulares auxiliares (RN-04, RIF-02-2).

Parte DETERMINISTA del sistema (no usa LLM): longitud de la respuesta y deteccion
de metricas cuantitativas con Regex para respaldar la dimension Resultado.

Limitaciones conocidas (mejorar en T-205): no distingue numeros no-metricos
("3 anios de carrera") ni cantidades escritas con palabras ("tres clientes").
"""
import re
from dataclasses import asdict, dataclass

_METRIC_RE = re.compile(
    r"""
    (?:\$\s?\d[\d.,]*(?:\s?(?:k|mil|millones|mxn|usd))?)          # montos: $1,500 / $2 millones
    |(?:\d+(?:[.,]\d+)?\s?%)                                       # porcentajes: 35% / 12.5 %
    |(?:\d+(?:[.,]\d+)?\s?(?:x|veces|usuarios|clientes|horas|dias|d\u00edas|semanas|meses|
        segundos|minutos|ms|k|mil|millones|pesos|mxn|usd|users|hours|days|weeks|months|
        personas|alumnos|ventas|errores|bugs|tickets)\b)           # cantidad + unidad
    |(?:(?!(?:19|20)\d{2}\b)\b\d{2,}\b)                            # numeros de 2+ digitos (no anios)
    """,
    re.IGNORECASE | re.VERBOSE,
)


@dataclass(frozen=True)
class AnswerFeatures:
    length_chars: int
    length_words: int
    metric_count: int
    has_metrics: bool

    def to_dict(self) -> dict:
        return asdict(self)


def extract_features(answer: str) -> AnswerFeatures:
    text = (answer or "").strip()
    metrics = _METRIC_RE.findall(text)
    return AnswerFeatures(
        length_chars=len(text),
        length_words=len(text.split()),
        metric_count=len(metrics),
        has_metrics=bool(metrics),
    )
