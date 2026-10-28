"""Almacen de sesiones. HOY: en memoria (sirve para demo/frontend). MANANA: Postgres (T-108).
La interfaz `SessionStore` es el contrato que debe respetar la implementacion Postgres."""
import uuid
from typing import Protocol


class SessionStore(Protocol):
    def create(self, state: dict) -> str: ...
    def get(self, session_id: str) -> dict | None: ...
    def save(self, session_id: str, state: dict) -> None: ...


class InMemorySessionStore:
    def __init__(self) -> None:
        self._data: dict[str, dict] = {}
        self.feedback: dict[str, list[dict]] = {}

    def create(self, state: dict) -> str:
        sid = str(uuid.uuid4())
        self._data[sid] = {**state, "session_id": sid}
        return sid

    def get(self, session_id: str) -> dict | None:
        return self._data.get(session_id)

    def save(self, session_id: str, state: dict) -> None:
        self._data[session_id] = state


store: SessionStore = InMemorySessionStore()
