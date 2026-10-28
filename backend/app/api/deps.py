"""Dependencias de FastAPI: RBAC. STUB DE DESARROLLO: el rol llega en la cabecera X-Role.
NO USAR EN PRODUCCION. TODO (ROADMAP T-114): autenticacion real (JWT/SSO institucional)."""
from fastapi import Header, HTTPException

from app.config import settings
from app.core.rbac import Permission, Role, has_permission


def require(permission: Permission):
    def checker(x_role: str = Header(default="student")) -> Role:
        if settings.auth_mode != "dev":
            raise HTTPException(501, "Autenticacion real pendiente (ROADMAP T-114)")
        try:
            role = Role(x_role)
        except ValueError:
            raise HTTPException(401, "Rol invalido") from None
        if not has_permission(role, permission):
            raise HTTPException(403, f"El rol '{role.value}' no tiene el permiso '{permission.value}'")
        return role
    return checker
