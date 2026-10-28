"""Monitor tecnico de errores de formato JSON (RN-09 / RNF-05 / RF-03 flujo 6A.2).

Skeleton: contador en memoria. TODO (ROADMAP T-702): exportar a metrica real
(Prometheus / tabla `tech_events`) y alertar si la tasa >= 0.5%.
"""
from dataclasses import dataclass

from app.core.constants import MAX_JSON_FORMAT_ERROR_RATE


@dataclass
class FormatErrorMonitor:
    attempts: int = 0
    failures: int = 0

    def record(self, ok: bool) -> None:
        self.attempts += 1
        if not ok:
            self.failures += 1

    @property
    def error_rate(self) -> float:
        return self.failures / self.attempts if self.attempts else 0.0

    def within_budget(self) -> bool:
        return self.error_rate < MAX_JSON_FORMAT_ERROR_RATE


format_monitor = FormatErrorMonitor()
