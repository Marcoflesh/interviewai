"""Estadistica pura (sin numpy) para la validacion contra el Golden Dataset (RN-07 / RNF-03 / RF-12).
Se comparte entre el backend y el notebook/script de Colab (RIN-03)."""
from math import sqrt

from app.core.constants import GOLDEN_MIN_CORRELATION


def pearson(x: list[float], y: list[float]) -> float:
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("Se requieren dos series del mismo largo (>= 2)")
    mx, my = sum(x) / n, sum(y) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    vx, vy = sum((a - mx) ** 2 for a in x), sum((b - my) ** 2 for b in y)
    return cov / sqrt(vx * vy) if vx and vy else 0.0


def _ranks(v: list[float]) -> list[float]:
    order = sorted(range(len(v)), key=lambda i: v[i])
    ranks, i = [0.0] * len(v), 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1       # rango promedio en empates
        i = j + 1
    return ranks


def spearman(x: list[float], y: list[float]) -> float:
    return pearson(_ranks(x), _ranks(y))


def quadratic_weighted_kappa(a: list[int], b: list[int], lo: int = 1, hi: int = 5) -> float:
    k = hi - lo + 1
    obs = [[0.0] * k for _ in range(k)]
    for x, y in zip(a, b):
        obs[x - lo][y - lo] += 1
    n = len(a)
    ha = [sum(r) for r in obs]
    hb = [sum(obs[i][j] for i in range(k)) for j in range(k)]
    num = den = 0.0
    for i in range(k):
        for j in range(k):
            w = (i - j) ** 2 / (k - 1) ** 2
            num += w * obs[i][j]
            den += w * ha[i] * hb[j] / n
    return 1 - num / den if den else 1.0


def passes_golden_gate(human: list[float], model: list[float], threshold: float = GOLDEN_MIN_CORRELATION) -> dict:
    """RN-07: la version del modelo solo pasa a produccion si Spearman >= 0.75 (D-06)."""
    rho = spearman(human, model)
    return {"spearman": round(rho, 4), "pearson": round(pearson(human, model), 4),
            "threshold": threshold, "approved": rho >= threshold, "n": len(human)}
