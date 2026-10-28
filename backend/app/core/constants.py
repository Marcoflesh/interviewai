"""Constantes del dominio de InterviewAI.

Fuente de verdad: SRS (docs/SRS.md). Cada constante indica la regla de negocio
(RN) o requisito no funcional (RNF) del que proviene. NO cambiar valores aqui
sin actualizar el SRS / docs/DECISIONS.md.
"""
from enum import Enum


class SessionStatus(str, Enum):
    """Estados de la sesion (RIF-01-2). `INICIADA` es adicional: ver DECISIONS.md D-03."""

    INICIADA = "iniciada"
    PROFUNDIZAR = "profundizar_pregunta"        # RN-03
    SIGUIENTE = "pasar_a_siguiente_tema"        # RN-05
    FINALIZADA = "finalizar_entrevista"         # RN-05 (nodo terminal)
    ABANDONADA = "abandonada"                   # RF-05 flujo alterno 1A


SCORE_MIN = 1                                   # RN-02
SCORE_MAX = 5                                   # RN-02
WEAK_THRESHOLD = 3                              # RN-03: < 3 en Accion o Resultado => profundizar
MIN_QUESTIONS = 5                               # RN-01
MAX_QUESTIONS = 10                              # RN-01

STAR_DIMENSIONS = ("situacion", "tarea", "accion", "resultado")        # RN-02
ALL_DIMENSIONS = STAR_DIMENSIONS + ("claridad_tecnica", "pertinencia")  # RN-02
DEEPEN_DIMENSIONS = ("accion", "resultado")                             # RN-03

GOLDEN_MIN_CORRELATION = 0.75                   # RN-07 / RNF-03
MAX_JSON_FORMAT_ERROR_RATE = 0.005              # RN-09 / RNF-05 (0.5%)
CSAT_TARGET = 0.80                              # RN-09 / RNF-06
TURN_LATENCY_BUDGET_S = 2.5                     # RNF-01
REPORT_LATENCY_BUDGET_S = 8.0                   # RNF-02
WEAKEST_ANSWERS_IN_REPORT = 2                   # RN-06
