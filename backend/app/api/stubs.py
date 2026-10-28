"""Endpoints PENDIENTES (501). Cada uno apunta al RF y a la tarea del ROADMAP que lo implementa."""
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import require
from app.core.rbac import Permission

router = APIRouter(prefix="/api", tags=["pendientes"])


def _todo(rf: str, task: str):
    raise HTTPException(501, f"Pendiente: {rf} (ROADMAP {task})")


@router.get("/students/me/history", dependencies=[Depends(require(Permission.VIEW_HISTORY))])
def history():  _todo("RF-07 historial y Tasa de Evolucion", "T-405")

@router.put("/rubrics", dependencies=[Depends(require(Permission.MANAGE_RUBRICS))])
def rubrics():  _todo("RF-08 catalogo de rubricas/recursos", "T-601")

@router.post("/golden", dependencies=[Depends(require(Permission.ANNOTATE_GOLDEN))])
def golden():  _todo("RF-09 Golden Dataset", "T-501")

@router.get("/hitl/queue", dependencies=[Depends(require(Permission.REVIEW_HITL))])
def hitl():  _todo("RF-10 Human-in-the-loop", "T-503")

@router.put("/admin/prompts", dependencies=[Depends(require(Permission.CONFIGURE_PROMPTS))])
def prompts():  _todo("RF-11 configuracion de prompts/grafo", "T-302")

@router.post("/admin/audits", dependencies=[Depends(require(Permission.RUN_AUDITS))])
def audits():  _todo("RF-12 validacion estadistica y auditoria de sesgos", "T-504")

@router.get("/admin/dashboard", dependencies=[Depends(require(Permission.VIEW_DASHBOARDS))])
def dashboard():  _todo("RF-13 tablero analitico", "T-602")
