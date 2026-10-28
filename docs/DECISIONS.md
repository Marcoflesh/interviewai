# Decisiones sobre ambigüedades del SRS
Cada una es una **suposición mía** donde el SRS no es explícito. Confirmar con el profesor/PO cuando se indique.

| ID | Tema | Decisión | Confirmar |
|---|---|---|---|
| D-01 | Turno final débil | Si `answered_count >= max_turns` se finaliza aunque Acción/Resultado <3 (RF-03 9A manda). | No |
| D-02 | ¿Cuentan los seguimientos? | Sí: toda respuesta evaluada cuenta para el total 5–10 (RN-01). Máx. **un** seguimiento por tema. | Sí |
| D-03 | Estado inicial | Se agrega `iniciada` a los estados de RIF-01-2. | No |
| D-04 | "Respuesta más débil" | Promedio de las 6 dimensiones; desempate: menor Resultado → menor Acción → turno más temprano. | Sí |
| D-05 | Tasa de Evolución de Puntaje | `(actual − promedio_previo) / promedio_previo × 100`. El SRS no la define. | **Sí (T-405)** |
| D-06 | Métrica del gate RN-07 | Spearman ≥ 0.75 (SRS dice "correlación o concordancia"); se reporta también Pearson. QWK implementado, sin usar en el gate. | Sí |
| D-07 | Permisos del Admin | Solo los listados en RIF-05-3 (no puede correr sesiones de estudiante). | No |
| D-08 | LLM por defecto | `FakeLLM` determinista para dev/pruebas; NO es un modelo real y no pasa el gate (Spearman 0.58 en el CSV de ejemplo). | No |
| D-09 | Persistencia temporal | `InMemorySessionStore` detrás de la interfaz `SessionStore`; se reemplaza en T-108. | No |
| D-10 | Reporte fuera del grafo | RF-05 es "punto de extensión" de RF-03; lo dispara la API. | No |
| D-11 | PDF | Fase inicial: `window.print()` + CSS de impresión. PDF desde backend en T-402 (RNF-02 < 8 s). | No |
| D-12 | Anonimización | Se aplica al CV **antes** de crear la sesión; las respuestas del chat aún no se anonimizan (T-106). | Sí |
