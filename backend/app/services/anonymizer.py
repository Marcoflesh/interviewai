"""Anonimizacion de datos personales (RN-10 / RNF-07 / RF-14).

Debe ejecutarse ANTES de guardar cualquier CV/texto en PostgreSQL.
Skeleton basado en Regex. TODO (ROADMAP T-106): NER para nombres/lugares
(spaCy es_core_news_md o Presidio) y pruebas de recall sobre CVs reales.
"""
import re
from dataclasses import dataclass, field

_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("URL", re.compile(r"(?:https?://|www\.|linkedin\.com/|github\.com/)\S+", re.I)),
    ("CURP", re.compile(r"\b[A-Z]{4}\d{6}[HM][A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z0-9]\d\b")),
    ("MATRICULA", re.compile(r"\bA0\d{7}\b")),   # matricula Tec, ej. A01709802
    ("TELEFONO", re.compile(r"(?<!\d)(?:\+?\d{1,3}[\s-]?)?\(?\d{2,3}\)?[\s-]?\d{3,4}[\s-]?\d{4}(?!\d)")),
]


@dataclass
class AnonymizationResult:
    text: str
    counts: dict[str, int] = field(default_factory=dict)


def anonymize(text: str, known_names: list[str] | None = None) -> AnonymizationResult:
    """Reemplaza PII por marcadores [EMAIL], [URL], etc. `known_names`: nombres
    conocidos del usuario (p. ej. el del perfil) a redactar como [NOMBRE]."""
    counts: dict[str, int] = {}
    out = text or ""
    for name in known_names or []:
        if name.strip():
            out, n = re.subn(re.escape(name.strip()), "[NOMBRE]", out, flags=re.I)
            if n:
                counts["NOMBRE"] = counts.get("NOMBRE", 0) + n
    for label, pattern in _PATTERNS:
        out, n = pattern.subn(f"[{label}]", out)
        if n:
            counts[label] = counts.get(label, 0) + n
    return AnonymizationResult(text=out, counts=counts)
