from app.core.rbac import Permission, Role, has_permission
from app.services.anonymizer import anonymize


def test_anonymize_pii():
    r = anonymize("Marco Perez, A01709802, marco@mail.com, 442 123 4567, https://linkedin.com/in/marco", ["Marco Perez"])
    for leaked in ["marco@mail.com", "A01709802", "442 123 4567", "linkedin.com/in", "Marco Perez"]:
        assert leaked not in r.text
    assert {"EMAIL", "MATRICULA", "TELEFONO", "URL", "NOMBRE"} <= set(r.counts)


def test_rbac_separation():
    assert has_permission(Role.STUDENT, Permission.RUN_SESSION)
    assert not has_permission(Role.STUDENT, Permission.CONFIGURE_PROMPTS)
    assert has_permission(Role.EXPERT, Permission.ANNOTATE_GOLDEN)
    assert not has_permission(Role.EXPERT, Permission.RUN_AUDITS)
    assert has_permission(Role.ADMIN, Permission.RUN_AUDITS)
