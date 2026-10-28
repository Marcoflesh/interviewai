# **Campus Querétaro**

# **SRS — InterviewAI: Simulador Inteligente de Entrevistas Laborales con Retroalimentación Personalizada**

**Marco Antonio Hernández Roque**  
**A01709802**  
**Profesor Ricardo Cortés Espinosa**  
**Materia Análisis de Requerimientos de Software**  
**Grupo 102**  
**Fecha de entrega: 27/10/2026**

# **Índice**

1. Norma de Referencia  
2. Necesidades de la Institución  
3. Requisito Objetivo  
4. Glosario de Términos  
5. Reglas de Negocio  
6. Requisitos Funcionales  
   * Estudiante / Candidato  
   * Product Owner / Evaluador Experto  
   * Administrador / Equipo MLOps  
   * Tabla de Priorización de Requisitos Funcionales  
7. Diagrama de Casos de Uso  
8. Descripción Requisitos Funcionales  
   * RF-03  
   * RF-05  
9. Diagrama de Actividades  
   * RF-03  
   * RF-05  
10. Interfaz GUI  
    * RF-03  
    * RF-05  
11. Requisitos No Funcionales  
12. Requisitos de Información  
    * RIF-01 (Sesiones de Entrevista — interview\_sessions)  
    * RIF-02 (Turnos de Conversación — message\_turns)  
    * RIF-03 (Evaluaciones del Modelo — model\_evaluations)  
    * RIF-04 (Retroalimentación del Usuario y Auditoría — user\_feedback y golden\_dataset)  
    * RIF-05 (Catálogo de Control de Acceso (RBAC))  
13. Requisitos de Interfaz  
    * Interfaz de Comunicación  
    * Interfaz Gráfica  
      * Vista Estudiante  
      * Vista Product Owner / Evaluador Experto  
      * Vista Administrador MLOps  
14. Conclusiones  
15. Referencias

# **Norma de Referencia**

La presente Especificación de Requisitos de Software (SRS) fue elaborada con base en los lineamientos de [ISO/IEC/IEEE 29148-2018](https://doi.org/10.1109/IEEESTD.2018.8559686).  
El documento adopta los lineamientos de dicha norma para la identificación, clasificación, organización y documentación de los requisitos de software.

# **Necesidades de la Institución**

Los estudiantes universitarios de últimos semestres y los recién egresados que buscan prácticas profesionales o su primer empleo formal enfrentan una situación complicada relacionada con la preparación y el desempeño en entrevistas laborales técnicas y conductuales. Debido a la falta de espacios seguros de práctica y a la dificultad de acceder de manera recurrente a mentores o reclutadores especializados, los alumnos suelen presentarse a procesos de selección con altos niveles de ansiedad y sin estructurar sus respuestas bajo metodologías estándar como el método STAR (Situación, Tarea, Acción y Resultado). Las áreas que representan mayor dificultad recurrente para los candidatos son la cuantificación de logros en la dimensión de Resultado, la descripción precisa de sus acciones individuales y la alineación de su experiencia académica con la descripción de la oferta laboral. Ante esta situación, resulta indispensable contar con una plataforma web interactiva y centralizada de autogestión que permita a los estudiantes simular entrevistas adaptadas a su perfil y vacante objetivo, recibiendo retroalimentación objetiva, inmediata y personalizada.  
Asimismo, desde la perspectiva tecnológica e institucional, una evaluación automatizada incorrecta conlleva un riesgo elevado: un falso positivo genera falsa confianza en el estudiante y lo lleva a fallar en su entrevista laboral real, mientras que un falso negativo produce frustración en el usuario.  
Como se muestra en el diagnóstico de necesidades ([Imagen 1 \- Diagnóstico de Necesidades InterviewAI](https://drive.google.com/file/d/1FZhNybz86fPaYdwCMSzBiIwup9sHgYLQ/view?usp=drivesdk)), el 74.2% de los estudiantes y recién egresados manifiesta una alta preocupación o ansiedad ante entrevistas técnicas y conductuales, mientras que el 65.5% desconoce o aplica sólo parcialmente la estructura STAR al responder. Asimismo, se identificó que los principales obstáculos son la falta de retroalimentación objetiva (48%), el desconocimiento de los criterios reales de evaluación por rol (32%) y la falta de métricas cuantitativas al exponer resultados (20%). Finalmente, el 68.4% reconoce no contar con seguimiento ni simulacros previos antes de postularse a una vacante.  
Los resultados presentan un patrón conjunto entre la ansiedad ante entrevistas laborales, la ausencia de práctica estructurada bajo el método STAR y la falta de retroalimentación inmediata. Su comportamiento conjunto evidencia la necesidad de centralizar la práctica en un simulador inteligente con validación estadística rigurosa que permita identificar áreas de mejora en tiempo real y ofrecer un Plan de Acción Personalizado al cierre de cada sesión.

# **Requisito Objetivo**

La plataforma web interactiva **InterviewAI**, estilizada mediante hojas de estilo en cascada ([CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)) y desplegada en contenedores de [Docker](https://docs.docker.com/guides/python/) para garantizar el control de versiones del entorno de Python, deberá proporcionar a los estudiantes universitarios de últimos semestres, recién egresados, Product Owner (reclutadores y profesores expertos) y administradores del equipo MLOps un entorno centralizado de autogestión, simulación y evaluación de entrevistas laborales. El núcleo del sistema operará mediante dos agentes basados en un modelo de lenguaje fundacional (Agente Entrevistador y Agente Evaluador conectados por API serverless) orquestados a través de grafos de estado en [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview), adaptando las preguntas al currículum y oferta laboral del usuario, calificando en tiempo real cada respuesta de 1 a 5 en estructura STAR, claridad técnica y pertinencia en un panel lateral de métricas en vivo, decidiendo dinámicamente si profundizar o cambiar de tema, y generando en menos de 8 segundos un reporte final descargable con ejemplos de mejora para las dos respuestas más débiles y un Plan de Acción Personalizado.

# **Glosario de Términos**

| Palabra | Significado |
| :---- | :---- |
| **InterviewAI** | Plataforma web interactiva de simulación de entrevistas laborales con retroalimentación personalizada mediante inteligencia artificial. |
| **Método STAR** | Metodología estructurada para responder preguntas de entrevistas por competencias, compuesta por cuatro dimensiones: Situación, Tarea, Acción y Resultado. |
| **LLM-as-a-Judge** | Enfoque en el que un modelo de lenguaje de gran tamaño (Agente Evaluador) califica respuestas abiertas utilizando plantillas de prompt estructuradas, ejemplos few-shot y salidas en formato JSON. |
| **Golden Dataset** | Conjunto de referencia de entre 50 y 100 respuestas estratificadas por área profesional y previamente calificadas por reclutadores y profesores expertos para validar la precisión del modelo. |
| **Human-in-the-loop** | Flujo operativo en el que expertos humanos revisan y etiquetan pares de pregunta-respuesta priorizados para mejorar el modelo en sus actualizaciones mensuales. |
| **RBAC** | Modelo de seguridad que restringe el acceso del sistema con base en los roles asignados a cada usuario ([IBM RBAC](https://www.ibm.com/mx-es/think/topics/rbac)). |
| **CSAT** | Indicador de satisfacción del usuario respecto a la utilidad percibida de la retroalimentación recibida en la plataforma. |
| **Regex** | Expresiones regulares utilizadas como característica tabular auxiliar para detectar la presencia de métricas cuantitativas en las respuestas del candidato. |
| **CSS (Cascading Style Sheets)** | Lenguaje de hojas de estilo utilizado para diseñar, maquetar y adaptar visualmente la interfaz gráfica web del simulador, el panel lateral de métricas STAR en vivo y las vistas de reportes ([MDN CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)). |
| **LangGraph** | Framework de orquestación basado en grafos de estado cíclicos que coordina el flujo de ejecución, la memoria de sesión y las transiciones condicionales entre el Agente Entrevistador y el Agente Evaluador ([LangGraph Docs](https://docs.langchain.com/oss/python/langgraph/overview)). |
| **Docker** | Plataforma de contenedorización que empaqueta el código, las librerías y una versión específica de Python en imágenes inmutables y versionadas para evitar conflictos de dependencias entre entornos ([Docker Python Docs](https://docs.docker.com/guides/python/)). |

# **Reglas de Negocio**

**RN-01 (Extensión de la sesión de entrevista):** Cada sesión de entrevista simulada debe integrar entre 5 y 10 respuestas evaluadas en tiempo real, adaptadas al currículum del candidato, al puesto objetivo y al nivel de seniority.  
**RN-02 (Vector de puntuación por respuesta):** El Agente Evaluador debe calificar cada respuesta del usuario mediante un vector de puntuación de 1 a 5 (\[1, 5\]) en tres dimensiones: estructura STAR (Situación, Tarea, Acción y Resultado), claridad técnica y pertinencia.  
**RN-03 (Decisión de profundización adaptativa):** Si el candidato obtiene una puntuación menor a 3 en las dimensiones de Acción o Resultado del método STAR, las aristas condicionales en el grafo de estados de LangGraph evalúan los puntajes STAR y activan el estado profundizar\_pregunta, pasando la transición del nodo Evaluador al nodo Entrevistador para generar una pregunta de seguimiento que profundice en su respuesta.  
**RN-04 (Extracción de características auxiliares):** El sistema debe extraer la longitud de la respuesta y detectar mediante expresiones regulares (Regex) la presencia de métricas cuantitativas para respaldar la evaluación del componente de Resultados en la metodología STAR.  
**RN-05 (Avance de tema y cierre de sesión):** Cuando la respuesta obtiene una puntuación mayor o igual a 3 en Acción y Resultado, o tras completarse la pregunta de seguimiento, las aristas condicionales en el grafo de estados de LangGraph evalúan el estado y determinan ejecutar la transición al nodo pasar\_a\_siguiente\_tema o, al concluir el número de turnos, pasar al nodo terminal finalizar\_entrevista.  
**RN-06 (Identificación de respuestas débiles y Plan de Acción):** Al finalizar la entrevista, el sistema debe identificar automáticamente las dos respuestas más débiles de la sesión, ofrecer ejemplos redactados de cómo mejorarlas y entregar un Plan de Acción Personalizado con recursos de estudio curados.  
**RN-07 (Criterio de despliegue con Golden Dataset):** Para aprobar el paso a producción de cualquier versión del modelo, el Agente Evaluador debe alcanzar una correlación o concordancia mínima de 0.75 frente a las calificaciones humanas del Golden Dataset (50 a 100 respuestas evaluadas por expertos).  
**RN-08 (Invariancia y ausencia de sesgo):** El vector de puntuación \[1, 5\] y la retroalimentación generada deben presentar 0% de contenido tóxico o sesgado, siendo invariantes al género, nacionalidad, edad o modismos regionales del candidato.  
**RN-09 (Umbrales de satisfacción y formato estructurado):** El sistema debe mantener una satisfacción con la retroalimentación (CSAT) superior al 80% y asegurar que los errores de formato en las salidas JSON sean inferiores al 0.5%.  
**RN-10 (Anonimización de datos personales):** Todo currículum y texto ingresado por el usuario debe procesarse mediante un pipeline automatizado de anonimización de datos personales antes de almacenarse en la base de datos interna.  
**RN-11 (Frecuencia de evaluación y monitoreo MLOps):** Los prompts y criterios de evaluación se deben revisar mensualmente o ante caídas de rendimiento, ejecutando pruebas diarias de 1 a 2 horas durante el desarrollo, evaluaciones de 24 a 48 horas en Google Colab antes del despliegue, revisión continua de métricas técnicas y revisión semanal de resultados de aprendizaje.  
**RN-12 (Control de versiones de entorno y aislamiento con Docker):** Todo componente del backend, grafo de agentes en LangGraph y pipeline de procesamiento deberá ejecutarse dentro de contenedores de Docker con una versión fija y estandarizada de Python, impidiendo discrepancias o fallos por incompatibilidad de versiones entre los entornos de desarrollo, pruebas y producción.

# **Requisitos Funcionales**

## **Estudiante / Candidato**

**RF-01:** Estudiante carga currículum vitae y descripción de oferta laboral objetivo.  
**RF-02:** Estudiante inicia sesión de entrevista simulada en el chat interactivo.  
**RF-03:** Sistema evalúa respuesta en tiempo real con método STAR y decide el estado de la sesión (profundizar\_pregunta, pasar\_a\_siguiente\_tema o finalizar\_entrevista) mediante el grafo de estados en LangGraph.  
**RF-04:** Estudiante consulta panel lateral de métricas STAR en vivo estilizado con CSS responsivo durante la entrevista.  
**RF-05:** Sistema genera reporte final descargable con las dos respuestas más débiles y Plan de Acción Personalizado.  
**RF-06:** Estudiante registra calificación de satisfacción (CSAT) sobre la retroalimentación recibida.  
**RF-07:** Estudiante consulta historial de sesiones y su Tasa de Evolución de Puntaje.

## **Product Owner / Evaluador Experto**

**RF-08:** Product Owner actualiza catálogo de rúbricas conductuales/técnicas y recursos de estudio por sector industrial.  
**RF-09:** Evaluador experto registra calificaciones de referencia en el Golden Dataset estratificado por carrera.  
**RF-10:** Evaluador experto revisa pares de pregunta-respuesta priorizados en el flujo Human-in-the-loop.

## **Administrador / Equipo MLOps**

**RF-11:** Ingeniero de ML configura el grafo de orquestación en LangGraph, las plantillas de prompt, ejemplos few-shot y esquemas JSON del Agente Entrevistador y Agente Evaluador.  
**RF-12:** Científico de Datos ejecuta validación estadística frente al Golden Dataset (correlación \>= 0.75) y auditoría de sesgos.  
**RF-13:** Analista de Datos consulta tablero de seguimiento segmentado por carrera, universidad y rol (CSAT, evolución de puntaje y motivos de abandono).  
**RF-14:** Ingeniero de Datos gestiona pipelines de extracción del banco de preguntas y anonimización de currículums en PostgreSQL.  
**RF-15:** Equipo MLOps y Full-Stack gestiona imágenes y contenedores versionados en Docker para estandarizar la versión de Python y sus dependencias.

## **Tabla de Priorización de Requisitos Funcionales**

| Requisito | Importancia | Dificultad | Riesgo | Estabilidad |
| :---- | :---- | :---- | :---- | :---- |
| **RF-03** | Alto | Alto | Alto | Medio |
| **RF-05** | Alto | Alto | Medio-alto | Medio-alto |
| **RF-12** | Alto | Alto | Alto | Medio |
| **RF-11** | Alto | Medio-alto | Medio-alto | Medio |
| **RF-01** | Alto | Medio | Medio-bajo | Alto |
| **RF-02** | Alto | Medio | Medio-bajo | Alto |
| **RF-04** | Alto | Medio | Bajo | Alto |
| **RF-08** | Medio-alto | Medio | Medio-bajo | Medio-alto |
| **RF-09** | Medio-alto | Medio | Medio | Alto |
| **RF-14** | Medio-alto | Medio-alto | Medio | Alto |
| **RF-13** | Medio-alto | Medio | Bajo | Alto |
| **RF-07** | Medio | Medio-bajo | Bajo | Alto |
| **RF-10** | Medio | Medio | Medio-bajo | Medio-alto |
| **RF-06** | Medio | Bajo | Bajo | Alto |
| **RF-15** | Alto | Medio | Bajo | Alto |

# **Diagrama de Casos de Uso**

# **Descripción Requisitos Funcionales**

## **RF-03**

| ID | RF-03 |
| :---- | :---- |
| **Nombre del caso de uso** | Sistema evalúa respuesta en tiempo real con método STAR y decide estado de la sesión |
| **Actor(es)** | Estudiante / Candidato, Orquestador LangGraph y API Motor LLM (Agente Evaluador y Agente Entrevistador) |
| **Descripción** | El backend de la plataforma, ejecutado dentro de un contenedor de Docker con control de versiones de Python, gestiona el estado de la sesión mediante un grafo de estados en LangGraph. Al recibir la respuesta del estudiante, extrae metadatos auxiliares (longitud de respuesta y métricas cuantitativas vía Regex) y los transfiere al nodo del Agente Evaluador junto con el prompt estructurado, rol objetivo, seniority y pregunta actual. El Agente Evaluador devuelve un JSON con la calificación \[1, 5\] en estructura STAR, claridad técnica y pertinencia. LangGraph evalúa las aristas condicionales para determinar el enrutamiento entre el nodo del Agente Evaluador y el nodo del Agente Entrevistador (decidiendo si profundizar en la pregunta cuando Acción o Resultado son menores a 3, pasar al siguiente tema o finalizar la entrevista), mientras la interfaz web estilizada con CSS renderiza de forma fluida la retroalimentación e indicadores en vivo. |
| **Pre condiciones** | 1\. El estudiante debe haber iniciado sesión en la plataforma web y cargado su currículum y oferta laboral (RF-01).2\. Debe existir una sesión de entrevista activa en curso (RF-02).3\. La conexión mediante API con el motor LLM (Gemini / OpenAI) debe estar configurada y activa.4\. El contenedor Docker del servicio backend con el entorno de Python y el grafo de LangGraph debe encontrarse en ejecución. |
| **Flujo** | 1\. El estudiante ingresa y envía su respuesta a la pregunta actual en el chat conversacional.2\. La plataforma registra el turno en la tabla message\_turns y ejecuta expresiones regulares (Regex) para calcular la longitud de la respuesta y detectar métricas cuantitativas.3\. El orquestador LangGraph actualiza el nodo de estado de la sesión construyendo la plantilla de prompt estructurada al concatenar el rol objetivo, el seniority, el historial resumido de la sesión, la pregunta actual, la respuesta del usuario y las características tabulares auxiliares.4\. El orquestador LangGraph envía el prompt al nodo del Agente Evaluador a través de la API del motor LLM.5\. El Agente Evaluador analiza la respuesta y genera una salida estructurada JSON con el vector de calificación \[1, 5\] en estructura STAR (Situación, Tarea, Acción, Resultado), claridad técnica y pertinencia, así como las fortalezas y áreas de mejora.6\. La plataforma valida que el JSON recibido cumpla con el esquema de formato establecido.7\. La plataforma guarda la evaluación en la tabla model\_evaluations, y el frontend actualiza las barras de progreso y badges de estado con estilos CSS en el panel lateral de métricas en vivo del estudiante.8\. El orquestador LangGraph evalúa la arista condicional verificando si las puntuaciones en las dimensiones de Acción y Resultado del método STAR son mayores o iguales a 3\.9\. El orquestador LangGraph actualiza el estado de la sesión y enruta la arista condicional hacia el estado pasar\_a\_siguiente\_tema.10\. El orquestador LangGraph activa el nodo del Agente Entrevistador para generar la siguiente pregunta personalizada y presentarla en el chat en un tiempo total menor a 2.5 segundos.11\. La plataforma finaliza el caso de uso del turno actual. |
| **Flujo alterno** | **6A Error de formato en la salida JSON del modelo**6A.1 La plataforma detecta que la respuesta devuelta por la API del LLM presenta un error de formato JSON.6A.2 La plataforma registra el evento en el monitor técnico (para supervisar que los errores sean menores al 0.5%) y solicita un reintento automático al Agente Evaluador.6A.3 Si el reintento tampoco es válido, la plataforma conserva el estado previo del turno y muestra el mensaje "No fue posible procesar la evaluación, intenta enviar tu respuesta nuevamente".6A.4 La plataforma finaliza el caso de uso.**8A Puntuación menor a 3 en Acción o Resultado**8A.1 La plataforma detecta que el estudiante obtuvo una calificación menor a 3 en la dimensión de Acción o en la dimensión de Resultado del método STAR.8A.2 La plataforma cambia el estado de la sesión a profundizar\_pregunta.8A.3 El Agente Entrevistador genera una pregunta de seguimiento adaptativa para que el estudiante profundice en las acciones tomadas o en los resultados cuantitativos obtenidos.8A.4 La plataforma muestra la pregunta de seguimiento en el chat y resalta el indicador correspondiente en el panel lateral en menos de 2.5 segundos.8A.5 La plataforma finaliza el caso de uso.**9A Último turno de la entrevista alcanzado**9A.1 La plataforma detecta que el estudiante ha completado el número total de preguntas de la sesión (entre 5 y 10 respuestas).9A.2 La plataforma actualiza el estado de la sesión a finalizar\_entrevista.9A.3 La plataforma invoca automáticamente la generación del reporte final (RF-05) y finaliza el caso de uso. |
| **Post condiciones** | 1\. La respuesta del estudiante y su vector de evaluación \[1, 5\] quedan almacenados en la base de datos PostgreSQL.2\. El panel lateral de métricas en vivo muestra las calificaciones actualizadas del turno.3\. El estado de la sesión queda actualizado (profundizar\_pregunta, pasar\_a\_siguiente\_tema o finalizar\_entrevista). |
| **Requerimientos especiales** | **Rendimiento:** Necesario porque la evaluación y generación de la siguiente pregunta en tiempo real debe completarse en menos de 2.5 segundos.**Equidad:** Necesario para garantizar que la evaluación sea justa, sin discriminación por género, edad, nacionalidad o modismos regionales. |
| **Puntos de extensión** | RF-05 (Generación de reporte final cuando el estado pasa a finalizar\_entrevista). |

## **RF-05**

| ID | RF-05 |
| :---- | :---- |
| **Nombre del caso de uso** | Sistema genera reporte final descargable con las dos respuestas más débiles y Plan de Acción Personalizado |
| **Actor(es)** | Estudiante / Candidato, API Motor LLM (Agente Evaluador) |
| **Descripción** | Al alcanzar el nodo terminal finalizar\_entrevista en LangGraph tras concluir los turnos de la entrevista simulada, la plataforma invoca el nodo de síntesis de reportes para analizar todas las evaluaciones registradas, seleccionar las dos respuestas con puntuación más baja y utilizar el Agente Evaluador para generar ejemplos concretos de mejora bajo el método STAR, integrando además un Plan de Acción Personalizado con recursos de estudio curados en un reporte descargable. La interfaz maqueta la vista comparativa y el plan de acción mediante reglas de CSS diseñadas para la visualización web y la exportación limpia a PDF en menos de 8 segundos. |
| **Pre condiciones** | 1\. El estudiante debe haber concluido entre 5 y 10 respuestas en la sesión activa, alcanzando el estado finalizar\_entrevista.2\. Las evaluaciones de cada turno deben encontrarse registradas en la tabla model\_evaluations. |
| **Flujo** | 1\. La plataforma detecta que el orquestador LangGraph ha alcanzado el nodo terminal del estado finalizar\_entrevista.2\. La plataforma consulta en PostgreSQL los turnos registrados en message\_turns y sus calificaciones en model\_evaluations.3\. La plataforma calcula la calificación global de la sesión, actualiza la Tasa de Evolución de Puntaje respecto a sesiones previas e identifica las dos respuestas más débiles del estudiante.4\. El orquestador LangGraph invoca el nodo de síntesis enviando al Agente Evaluador las dos respuestas más débiles junto con la rúbrica del rol y el catálogo de recursos de estudio curados por el Product Owner.5\. El Agente Evaluador genera ejemplos redactados de cómo mejorar ambas respuestas aplicando correctamente Situación, Tarea, Acción y Resultado, y selecciona las recomendaciones de estudio personalizadas.6\. La plataforma valida que la información del reporte esté completa y bien estructurada en un tiempo menor a 8 segundos.7\. La plataforma almacena el reporte final en la base de datos interna y despliega en pantalla la vista del Reporte Final y Plan de Acción Personalizado estilizada con reglas CSS responsivas.8\. El estudiante consulta sus fortalezas, la comparativa de sus dos respuestas más débiles y las recomendaciones de estudio.9\. El estudiante selecciona el botón "Descargar Reporte PDF".10\. La plataforma genera y descarga el archivo PDF en el dispositivo del usuario y muestra el módulo de retroalimentación de satisfacción (CSAT).11\. La plataforma finaliza el caso de uso. |
| **Flujo alterno** | **1A Abandono de la sesión antes de finalizar**1A.1 El estudiante abandona el chat antes de responder el mínimo de 5 preguntas de la entrevista.1A.2 La plataforma registra el estado de abandono en interview\_sessions para el análisis de motivos de abandono del Analista de Datos.1A.3 La plataforma no genera el reporte final completo y finaliza el caso de uso.**6A Error o demora en la síntesis del reporte por la API del LLM**6A.1 La plataforma detecta que la API del motor LLM no responde dentro del umbral o devuelve un formato inválido.6A.2 La plataforma realiza un reintento inmediato y, en caso de persistir el fallo, presenta el resumen cuantitativo de las calificaciones ya almacenadas en la sesión junto con el botón "Reintentar generación de ejemplos STAR".6A.3 La plataforma finaliza el caso de uso. |
| **Post condiciones** | 1\. El reporte final con el análisis de las dos respuestas más débiles y el Plan de Acción Personalizado queda registrado en PostgreSQL y disponible para descarga.2\. Los indicadores de entrevistas completadas y evolución de puntaje entre sesiones quedan actualizados. |
| **Requerimientos especiales** | **Rendimiento:** El reporte final completo debe generarse en menos de 8 segundos. |
| **Puntos de extensión** | RF-06 (Registro de satisfacción con la retroalimentación CSAT). |

# **Diagrama de Actividades**

## **RF-03**

## **RF-05**

# **Interfaz GUI**

## **RF-03**

## **RF-05**

# **Requisitos No Funcionales**

**RNF-01 (Rendimiento por turno):** El tiempo de respuesta del sistema para evaluar cada intervención del usuario y generar la siguiente pregunta durante la entrevista simulada deberá ser menor a 2.5 segundos.  
**RNF-02 (Rendimiento del reporte final):** El reporte final de la sesión y el Plan de Acción Personalizado deberán generarse en menos de 8 segundos tras concluir la entrevista.  
**RNF-03 (Precisión y concordancia estadística):** El Agente Evaluador deberá alcanzar y mantener una correlación o concordancia mínima de 0.75 entre sus calificaciones y las calificaciones humanas del Golden Dataset (50 a 100 respuestas evaluadas por expertos) antes de su despliegue.  
**RNF-04 (Equidad y no discriminación):** El sistema deberá garantizar 0% de contenido tóxico o sesgado en las evaluaciones, manteniendo invariancia frente al género, edad, nacionalidad o modismos regionales del candidato.  
**RNF-05 (Confiabilidad de formato):** La tasa de errores de formato en las salidas estructuradas JSON de los agentes LLM deberá ser inferior al 0.5%.  
**RNF-06 (Usabilidad, diseño en CSS y satisfacción):** La plataforma web deberá implementar una interfaz gráfica maquetada con CSS modular y responsivo (con barras de progreso dinámicas y alertas cromáticas por dimensión STAR) que permita una navegación fluida y alcance una satisfacción con la retroalimentación (CSAT) superior al 80%.  
**RNF-07 (Seguridad y privacidad):** El sistema deberá implementar control de acceso basado en roles (RBAC) y ejecutar la anonimización automática de datos personales sobre todos los currículums cargados antes de guardarlos en PostgreSQL.  
**RNF-08 (Mantenibilidad MLOps y orquestación con LangGraph):** La plataforma deberá gestionar el flujo conversacional y de evaluación mediante grafos modulares en LangGraph, permitiendo la revisión mensual de nodos, prompts y criterios de evaluación mediante scripts automatizados en Google Colab (pruebas diarias de 1 a 2 horas en desarrollo y evaluaciones de 24 a 48 horas previo al despliegue).  
**RNF-09 (Portabilidad y control de versiones con Docker):** El sistema deberá empaquetarse y distribuirse mediante contenedores de Docker con archivos Dockerfile y docker-compose versionados que fijen la versión exacta de Python y todas las librerías del proyecto, eliminando conflictos de compatibilidad entre sistemas operativos y entornos de despliegue.

# **Requisitos de Información**

## **RIF-01 (Sesiones de Entrevista — interview\_sessions)**

**RIF-01-1 Datos del Perfil y Contexto:** ID de sesión, ID de estudiante, carrera, universidad, rol objetivo, nivel de seniority, texto de currículum anonimizado, descripción de la oferta laboral.  
**RIF-01-2 Estado y Seguimiento de la Sesión:** Estado actual (profundizar\_pregunta, pasar\_a\_siguiente\_tema, finalizar\_entrevista, abandonada), fecha de inicio y término, calificación global de la sesión, Tasa de Evolución de Puntaje.

## **RIF-02 (Turnos de Conversación — message\_turns)**

**RIF-02-1 Registro de Mensajes:** ID de turno, ID de sesión, número de pregunta \[1 a 10\], pregunta emitida por el Agente Entrevistador, respuesta del candidato.  
**RIF-02-2 Características Tabulares Auxiliares:** Longitud de la respuesta, presencia y conteo de métricas cuantitativas detectadas mediante expresiones regulares, tiempo de respuesta en segundos.

## **RIF-03 (Evaluaciones del Modelo — model\_evaluations)**

**RIF-03-1 Vector de Calificación \[1, 5\]:** Puntuación en Situación, Tarea, Acción y Resultado del método STAR, puntuación en claridad técnica, puntuación en pertinencia.  
**RIF-03-2 Retroalimentación y Plan de Mejora:** Fortalezas detectadas, áreas de mejora, indicador de respuesta débil, ejemplo de respuesta mejorada y recursos recomendados del Plan de Acción Personalizado.

## **RIF-04 (Retroalimentación y Validación — user\_feedback y golden\_dataset)**

**RIF-04-1 Satisfacción del Usuario:** ID de evaluación CSAT, ID de sesión, utilidad percibida de la retroalimentación, comentario del estudiante, motivo de abandono.  
**RIF-04-2 Catálogo de Golden Dataset y Rúbricas:** ID de respuesta experta, área profesional, rúbrica conductual/técnica asociada, calificación humana, calificación del modelo, estado de revisión Human-in-the-loop.

## **RIF-05 (Catálogo de Control de Acceso (RBAC))**

**RIF-05-1 Rol Estudiante / Candidato:** Permisos limitados a la carga de su currículum y oferta laboral, interacción con el chat de simulación, consulta de su panel lateral de métricas en vivo y descarga de sus reportes finales.  
**RIF-05-2 Rol Product Owner / Evaluador Experto:** Permisos para definir y actualizar las rúbricas conductuales y técnicas por industria, curar las fuentes de recursos de estudio y anotar el Golden Dataset estratificado.  
**RIF-05-3 Rol Administrador / Equipo MLOps:** Permisos totales sobre la configuración de plantillas de prompt de los agentes LLM, ejecución de auditorías estadísticas en Google Colab, administración de tablas en PostgreSQL y consulta de tableros analíticos segmentados.

# **Requisitos de Interfaz**

## **Interfaz de Comunicación**

**RIN-01 (Orquestación en LangGraph y Conexión API con Motor LLM):** La plataforma deberá gestionar el ciclo de vida de los agentes mediante un grafo de estados en LangGraph que se comunique por API en la nube con GPU serverless (Gemini / OpenAI) empleando plantillas de prompt estructuradas y salidas JSON.  
**RIN-02 (Base de datos PostgreSQL):** El backend deberá conectarse de forma segura a la base de datos interna en PostgreSQL para gestionar las tablas productivas interview\_sessions, message\_turns, model\_evaluations y user\_feedback, así como el pipeline de anonimización.  
**RIN-03 (Integración con Google Colab):** El sistema deberá permitir la conexión de scripts de evaluación automatizada desde Google Colab para ejecutar las pruebas pre-despliegue y mensuales frente al Golden Dataset.  
**RIN-04 (Infraestructura de Contenedores Docker):** Los servicios de frontend (HTML/CSS), backend en Python, orquestador LangGraph y conexión a PostgreSQL deberán comunicarse a través de una red interna definida en Docker para asegurar el aislamiento y la consistencia de versiones de Python.

## **Interfaz Gráfica**

Todas las vistas de la plataforma están construidas y estilizadas con hojas de estilo CSS responsivas (Grid y Flexbox) para garantizar legibilidad, jerarquía visual en las tarjetas de KPIs y actualización fluida del panel de métricas STAR en vivo:

### **Vista Estudiante**

### **Vista Product Owner / Evaluador Experto**

### **Vista Administrador MLOps**

# **Conclusiones**

A lo largo de la elaboración de esta Especificación de Requisitos de Software (SRS) para el proyecto **InterviewAI**, fue posible estructurar de manera formal todas las dimensiones técnicas, operativas y de negocio planteadas en el Machine Learning Canvas y en la definición de roles MLOps bajo el estándar ISO/IEC/IEEE 29148-2018. Traducir un sistema basado en dos agentes de inteligencia artificial (Agente Entrevistador y Agente Evaluador) orquestados mediante LangGraph, maquetados con CSS para una interfaz intuitiva y aislados con Docker para garantizar el control de versiones de Python a reglas de negocio, casos de uso y requisitos verificables permitió establecer límites claros entre la lógica determinista de la plataforma web (como la extracción de métricas cuantitativas con expresiones regulares y el control de estados de la sesión) y el comportamiento probabilístico del modelo de lenguaje.  
En cuanto al impacto para los estudiantes universitarios de últimos semestres y recién egresados, este documento demuestra que el valor de una herramienta de preparación laboral no reside únicamente en generar preguntas automatizadas, sino en garantizar que la retroalimentación sea objetiva, rápida (menor a 2.5 segundos por turno) y estadísticamente confiable. La exigencia de validar el enfoque LLM-as-a-Judge frente a un Golden Dataset anotado por reclutadores y profesores expertos con una correlación mínima de 0.75, junto con la auditoría de 0% de sesgos por género, edad o nacionalidad, evita el riesgo de generar falsa confianza o frustración en el alumno.  
Finalmente, la articulación de las responsabilidades del Ingeniero de ML, Desarrollador Full-Stack, Científico de Datos, Product Owner, Analista de Datos e Ingeniero de Datos dentro de los requisitos funcionales, no funcionales y de información consolida una arquitectura integral. De esta manera, **InterviewAI** no sólo brinda un espacio seguro para reducir la ansiedad ante entrevistas laborales, sino que asegura una mejora medible en el desempeño de los candidatos a través de su Plan de Acción Personalizado y el monitoreo continuo de su evolución entre sesiones.

# **Referencias**

16. International Organization for Standardization, International Electrotechnical Commission, & Institute of Electrical and Electronics Engineers. (2018). Systems and software engineering—Life cycle processes—Requirements engineering (ISO/IEC/IEEE Standard 29148:2018). [https\://doi.org/10.1109/IEEESTD.2018.8559686](https://doi.org/10.1109/IEEESTD.2018.8559686)  
17. Kosinski, G. L. M. (2025, 26 noviembre). ¿Qué es el control de acceso basado en roles (RBAC)? IBM. [https\://www\.ibm.com/mx-es/think/topics/rbac](https://www.ibm.com/mx-es/think/topics/rbac)  
18. Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. Advances in Neural Information Processing Systems (NeurIPS). [https\://arxiv.org/abs/2306.05685](https://arxiv.org/abs/2306.05685)  
19. Docker Inc. (2026). *Python language-specific guide — Docker Documentation*. [https\://docs.docker.com/guides/python/](https://docs.docker.com/guides/python/)  
20. LangChain Inc. (2026). *LangGraph Overview: Agent Orchestration Framework*. [https\://docs.langchain.com/oss/python/langgraph/overview](https://docs.langchain.com/oss/python/langgraph/overview)  
21. Mozilla Developer Network (MDN). (2025). *CSS: Cascading Style Sheets*. [https\://developer.mozilla.org/en-US/docs/Web/CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)








