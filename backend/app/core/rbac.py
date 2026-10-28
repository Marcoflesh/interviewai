"""RBAC (RNF-07 / RIF-05).

Tres roles del SRS -> conjunto de permisos. La autenticacion real NO esta
implementada (ver ROADMAP T-114); `app/api/deps.py` trae un stub de desarrollo.
"""
from enum import Enum


class Role(str, Enum):
    STUDENT = "student"   # RIF-05-1 Estudiante / Candidato
    EXPERT = "expert"     # RIF-05-2 Product Owner / Evaluador Experto
    ADMIN = "admin"       # RIF-05-3 Administrador / Equipo MLOps


class Permission(str, Enum):
    # Estudiante (RIF-05-1)
    UPLOAD_CV = "upload_cv"
    RUN_SESSION = "run_session"
    VIEW_LIVE_METRICS = "view_live_metrics"
    DOWNLOAD_REPORT = "download_report"
    SUBMIT_CSAT = "submit_csat"
    VIEW_HISTORY = "view_history"
    # Product Owner / Evaluador Experto (RIF-05-2)
    MANAGE_RUBRICS = "manage_rubrics"
    CURATE_RESOURCES = "curate_resources"
    ANNOTATE_GOLDEN = "annotate_golden"
    REVIEW_HITL = "review_hitl"
    # Admin / MLOps (RIF-05-3)
    CONFIGURE_PROMPTS = "configure_prompts"
    RUN_AUDITS = "run_audits"
    MANAGE_DB = "manage_db"
    VIEW_DASHBOARDS = "view_dashboards"
    MANAGE_CONTAINERS = "manage_containers"


ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.STUDENT: frozenset({
        Permission.UPLOAD_CV, Permission.RUN_SESSION, Permission.VIEW_LIVE_METRICS,
        Permission.DOWNLOAD_REPORT, Permission.SUBMIT_CSAT, Permission.VIEW_HISTORY,
    }),
    Role.EXPERT: frozenset({
        Permission.MANAGE_RUBRICS, Permission.CURATE_RESOURCES,
        Permission.ANNOTATE_GOLDEN, Permission.REVIEW_HITL,
    }),
    Role.ADMIN: frozenset({
        Permission.CONFIGURE_PROMPTS, Permission.RUN_AUDITS, Permission.MANAGE_DB,
        Permission.VIEW_DASHBOARDS, Permission.MANAGE_CONTAINERS,
    }),
}


def has_permission(role: Role, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, frozenset())
