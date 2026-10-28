"""OllamaLLM contra un servidor HTTP falso (no requiere Ollama instalado)."""
import json, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import pytest
from app.schemas.evaluation import parse_evaluation
from app.services.llm_client import LLMUnavailableError, OllamaLLM, list_ollama_models

EVAL = {"situacion": 3, "tarea": 3, "accion": 4, "resultado": 2, "claridad_tecnica": 3, "pertinencia": 3}
seen = {}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, obj):
        data = json.dumps(obj).encode(); self.send_response(200)
        self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(data)
    def do_GET(self): self._send({"models": [{"name": "qwen2.5:7b"}, {"name": "llama3.1:8b"}]})
    def do_POST(self):
        seen.update(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
        self._send({"message": {"role": "assistant", "content": json.dumps(EVAL)}})


@pytest.fixture(scope="module")
def url():
    srv = HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_port}"; srv.shutdown()


def test_chat_json_mode_and_models(url):
    out = OllamaLLM(url, "qwen2.5:7b").complete("evaluator.evaluate", "sys", "usr", json_mode=True)
    assert parse_evaluation(out).accion == 4 and seen["format"] == "json" and seen["model"] == "qwen2.5:7b"
    assert list_ollama_models(url) == ["qwen2.5:7b", "llama3.1:8b"]


def test_unavailable_raises():
    with pytest.raises(LLMUnavailableError):
        OllamaLLM("http://127.0.0.1:1", "x", timeout=1).complete("interviewer.first", "s", "u")
