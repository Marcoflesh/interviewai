from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)
BODY = {"target_role": "Desarrollador Backend", "seniority": "junior", "num_questions": 5,
        "cv_text": "Estudiante de ISC, correo a@b.com, proyectos en Python y SQL.",
        "job_description": "Buscamos practicante backend con Python y bases de datos."}
STRONG = ("Lidere la migracion del sistema; yo disene el esquema, implemente scripts y capacite a 12 personas, "
          "reduciendo 40% el tiempo de captura en 3 semanas. ") * 2


def test_health_and_rbac():
    assert c.get("/health").json()["status"] == "ok"
    assert c.get("/api/admin/dashboard").status_code == 403            # estudiante no ve el tablero
    assert c.get("/api/admin/dashboard", headers={"X-Role": "admin"}).status_code == 501


def test_full_flow_to_report():
    r = c.post("/api/sessions", json=BODY).json()
    assert r["anonymization"].get("EMAIL") == 1
    sid, status = r["session_id"], "iniciada"
    while status != "finalizar_entrevista":
        a = c.post(f"/api/sessions/{sid}/answer", json={"answer": STRONG}).json()
        status = a["status"]
    assert a["report_ready"] and a["answered_count"] == 5
    rep = c.get(f"/api/sessions/{sid}/report").json()
    assert len(rep["weakest_answers"]) == 2
    assert c.post(f"/api/sessions/{sid}/feedback", json={"csat": 5}).json() == {"ok": True}
    assert c.post(f"/api/sessions/{sid}/answer", json={"answer": "x"}).status_code == 409
