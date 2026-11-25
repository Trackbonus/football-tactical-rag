# Resumen del corpus para diseñar preguntas de evaluación

## Alcance y método

El archivo `resultados/chunks_semanticos.json` contiene **5.487 fragmentos** procedentes de **50 documentos**. Se revisaron sus textos, metadatos `source`/`page` y, como índice auxiliar, los registros disponibles en `inventario_corpus.csv` e `inventario.txt`. Las referencias de páginas que siguen son las páginas asignadas durante la extracción de PDF.

Los temas se solapan: un fragmento de presión tras pérdida puede tratar también transiciones, y uno de redes de pase puede mencionar formación y posesión. La distribución de la tabla es una **estimación por marcadores temáticos en el texto real** (términos en inglés y español más comprobación de los documentos núcleo), no una partición exclusiva ni una clasificación manual perfecta. Los conteos de fragmentos indican dónde hay señales textuales del tema; los documentos núcleo son los que desarrollan el tema de forma sostenida. Las cantidades son adecuadas para orientar una selección de preguntas, no para afirmar prevalencia científica.

## Inventario y distribución temática

| Tema | Fragmentos con señales del tema (aprox.) | Documentos con señales (aprox.) | Documentos núcleo |
|---|---:|---:|---|
| Organización defensiva, presión, contrapresión y rest defence | 385 | 28 | 5–7 |
| Transiciones y contraataques | 159 | 26 | 6–8 |
| Posesión, construcción y circulación/pases | 234 | 35 | 8–10 |
| Sistemas, formaciones y cambios de sistema | 136 | 15 | 5–7 |
| Estilos de juego y contexto | 289 | 38 | 5–7 |
| Ataques, indicadores ofensivos y ocasiones de gol | 179 | 33 | 5–7 |
| Balón parado (córneres, tiros libres, saques de banda) | 281 | 22 | 6–8 |
| Principios tácticos, espacio, dinámica colectiva y roles | 96 | 15 | 5–8 |
| Decisiones de entrenadores, rival y gestión del partido | 135 | 25 | 3–5 |
| Análisis de rendimiento, tracking, redes, IA y entrenamiento | 417 | 34 | 8–12 |

> Los fragmentos se cuentan por tema y pueden aparecer en varias filas. Los términos amplios —por ejemplo, “defensa”, “estilo” o “análisis”— generan menciones incidentales; por eso el conteo no sustituye la lectura de las fuentes núcleo.

## Temas, fuentes y contenido utilizable

### 1. Organización defensiva, presión, contrapresión y rest defence

**Fuentes principales:** `counterpressing.pdf` (pp. 1–41); `A rule-based approach to classify counterpressing … rest defence.pdf` (pp. 1–18); `10.1515_jqas-2026-0001.pdf` (pp. 1–13); `17479541221075734.pdf` (pp. 1–27); Forcher et al., `forcher-et-al-2023-is-a-compact-organization-important-for-defensive-success-in-elite-soccer-analysis-based-on-player.pdf` (pp. 1–13).

**Contenido:** definiciones operativas de presión y contrapresión; detección de contrapresión con datos posicionales y de eventos; relación entre presión, recuperación/pérdida de balón y territorio; compactación y coordinación defensiva; rest defence como organización de seguridad mientras el equipo ataca. El estudio de rest defence distingue concesión de territorio y de remates: sus resultados no deben convertirse en una afirmación general de que la contrapresión evita tiros. La revisión de tracking advierte heterogeneidad en cómo se definen y miden las acciones defensivas.

**Preguntas viables:**
- **Definición:** ¿Qué diferencia hay entre presión alta y contrapresión tras perder el balón según las fuentes?
- **Explicación:** ¿Qué función cumple la rest defence mientras un equipo ataca y qué riesgos intenta limitar?
- **Comparación:** ¿Qué resultados se reportan para la contrapresión frente a la organización compacta, y qué indicadores no deben confundirse?

### 2. Transiciones y contraataques

**Fuentes principales:** `s12662-024-00951-9.pdf` (pp. 1–11); `FIFA_Session_Plan_Urias_counter.pdf` (pp. 1–5); `counterpressing.pdf` (pp. 1–41); `10.1515_jqas-2026-0001.pdf` (pp. 1–13); `ocasiones_de_gol.pdf` (pp. 1–11).

**Contenido:** transiciones ofensivas y defensivas como fases de cambio de posesión; distintas definiciones de cuándo comienzan y terminan; progresión rápida, toma de decisiones, carreras de apoyo y uso del espacio tras recuperar; interdependencia entre acciones atacantes y organización rival. La revisión de transiciones compila resultados de estudios previos, no una ley universal. El plan FIFA aporta ejercicios y consignas de entrenamiento —por ejemplo, temporización de pases, desmarques y apertura de espacio—, que son material práctico, no evidencia experimental.

**Preguntas viables:**
- **Definición:** ¿Qué problemas de definición existen al determinar el inicio y final de una transición?
- **Explicación:** ¿Qué acciones y condiciones describe el plan de sesión FIFA para progresar en un contraataque?
- **Síntesis:** ¿Cómo se relacionan la recuperación, el espacio disponible y la organización defensiva rival en una transición, según las fuentes?

### 3. Posesión, construcción y circulación/pases

**Fuentes principales:** `deb-et-al-2024-creating-an-augmented-possession-framework-to-evaluate-phases-of-play-and-application-in-international.pdf` (pp. 1–11); `FIFA_Session_Plan_Skinner.pdf` (pp. 1–8); `In modern football.pdf` (pp. 1–7); `En función del esquema por el que opte el entrenador.pdf` (pp. 1–5); `ijerph-17-09396.pdf` (pp. 1–15); `41598_2025_Article_4507.pdf` (pp. 1–14); `ijerph-17-06649.pdf` (pp. 1–15).

**Contenido:** evaluación de la posesión por fases (primera fase, progresión/segunda fase, fase final y transición defensa-ataque); construcción desde atrás y avance por tercios; patrones de movimiento frente a distintos sistemas; relación entre pasador y receptor; redes de pases y distribución espacial. Los planes FIFA describen tareas concretas para superar presión y progresar por zonas; los artículos de redes describen métricas o patrones asociados a contextos, no recetas universales.

**Preguntas viables:**
- **Definición:** ¿Qué fases distingue el marco de posesión aumentada y qué permite evaluar cada una?
- **Explicación:** ¿Qué patrones de movimiento propone el material de construcción desde atrás ante un 5-3-2?
- **Comparación:** ¿Qué diferencias hay entre evaluar pases individuales y analizar una red de pases del equipo?

### 4. Sistemas, formaciones y cambios de sistema

**Fuentes principales:** Bauer et al., `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf` (pp. 1–21); `13102_2026_Article_1657.pdf` (pp. 1–9); `fpsyg-13-914915.pdf` (pp. 1–11); `pone.0210191.pdf` (pp. 1–12); `fspor-6-1512386.pdf` (pp. 1–15); `tt_systems_of_play.pdf` (pp. 1–2).

**Contenido:** formaciones como estructuras contextuales y dinámicas; identificación de sistemas a partir de datos posicionales; cambios durante el partido; comparación experimental de 4-2-3-1 y 3-5-2; distribución y resultados asociados a formaciones en varias ligas; sesión práctica con 4-4-2, 3-5-2, 4-3-3/3-4-3 y 4-5-1. El material de sistemas de juego expone decisiones y trade-offs de entrenamiento; los estudios observacionales describen asociaciones, no causalidad de la formación sobre ganar.

**Preguntas viables:**
- **Definición:** ¿Qué información permite identificar la estructura de una formación además de su etiqueta numérica?
- **Comparación:** ¿Qué diferencias reporta el estudio 11v11 entre 4-2-3-1 y 3-5-2 en las variables medidas?
- **Interpretación:** ¿Por qué las fuentes describen las formaciones como dependientes del contexto y de los objetivos del partido?

### 5. Estilos de juego y contexto

**Fuentes principales:** `estilos_de_juego.pdf` (pp. 1–16); `plakias-et-al-2024-a-grounded-theory-for-professional-soccer-teams-playing-styles-towards-a-consensus.pdf` (pp. 1–14); `contexto_estilos.pdf` (pp. 1–22); `produccion_retos,+Retos+56+(179-187)+104182+esp..pdf` (pp. 1–9); `jfmk-09-00088.pdf` (pp. 1–13); `s41598-019-49969-2.pdf` (pp. 1–14).

**Contenido:** revisiones sobre cómo definir y medir estilos; marcos de consenso para describir estilos de equipos profesionales; variables contextuales que influyen en el estilo; indicadores tácticos en situaciones de juego; análisis de equipos de Guardiola y del Barcelona histórico mediante secuencias y redes. El corpus permite comparar definiciones, criterios y casos concretos, pero los resultados de un equipo/temporada no se generalizan automáticamente.

**Preguntas viables:**
- **Definición:** ¿Qué dificultades señalan las revisiones al definir y medir un estilo de juego?
- **Comparación:** ¿Qué diferencias de secuencias de posesión describe el estudio entre Barcelona y Manchester City de Guardiola?
- **Síntesis:** ¿Cómo puede el contexto del partido cambiar la interpretación de un estilo de juego?

### 6. Ataques, indicadores ofensivos y ocasiones de gol

**Fuentes principales:** `ocasiones_de_gol.pdf` (pp. 1–11); `fspor-06-1473311.pdf` (pp. 1–11); `The_tactics_of_successful_attacks_in_professional_association_football_large_scale_spatiotemporal_analysis_of_dynamic_subgroups_using_position_tracking_data.pdf` (pp. 1–12); `jfmk-09-00088.pdf` (pp. 1–13); `s12662-024-00951-9.pdf` (pp. 1–11).

**Contenido:** indicadores tácticos asociados a posesiones que terminan en ocasión; posición y organización del rival; patrones de ataque directo en Premier League y La Liga; coordinación y sincronía de subgrupos durante ataques exitosos; métricas de rendimiento y goles/remates. Hay resultados específicos de muestras, ligas y operacionalizaciones. Una asociación entre un indicador y una ocasión no prueba que ese indicador por sí solo cause la ocasión.

**Preguntas viables:**
- **Definición:** ¿Qué se considera una posesión que genera una ocasión en el estudio de ocasiones de gol?
- **Explicación:** ¿Qué variables del rival y de la acción ofensiva analiza ese estudio?
- **Comparación/síntesis:** ¿Qué aportan los análisis de ataque directo y de coordinación de subgrupos, y qué miden de forma distinta?

### 7. Balón parado: córneres, tiros libres y saques de banda

**Fuentes principales:** `applsci-15-04984.pdf` (pp. 1–20; córneres); `Unlocking the power a field.pdf` (pp. 1–25; revisión de balón parado); `Art+233.pdf` (pp. 1–7; saques de banda); `pone.0294317.pdf` (pp. 1–14; saques de banda); `16752019005.pdf` (pp. 1–11; tiros libres indirectos); `pone.0243287.pdf` (pp. 1–20; barrera y visión del portero ante tiros libres directos).

**Contenido:** factores de ejecución y organización en córneres; envíos centrales, movimientos ofensivos y estructuras defensivas; frecuencia y limitaciones de la evidencia sobre distintas acciones a balón parado; dirección, distancia, velocidad, presión y zona en saques de banda; análisis multivariante de tiros libres indirectos del Mundial 2014; estudio de laboratorio/realidad virtual sobre oclusión visual del portero por la barrera. No mezclar tipos de balón parado: cada fuente aborda una situación y un resultado particular.

**Preguntas viables:**
- **Comparación:** ¿Qué factores se estudian en córneres frente a saques de banda?
- **Explicación:** ¿Qué acciones y variables del saque de banda se relacionan con conservar o perder la posesión?
- **Síntesis:** ¿Qué puede afirmarse sobre la barrera y la visión del portero en tiros libres, y cuáles son los límites del estudio experimental?

### 8. Principios tácticos, espacio, dinámica colectiva y roles

**Fuentes principales:** `hukin-58-207.pdf` (pp. 1–8; principios tácticos por edades); `rechenchoskyetal2017.pdf` (pp. 1–9; eficiencia por posiciones); `pone.0180773.pdf` (pp. 1–16; espacio de interacción); `The_tactics_of_successful_attacks_…pdf` (pp. 1–12; subgrupos); `barraclough-et-al-2023-creating-a-shared-mental-model-of-performance-coaches-perspectives-of-key-position-specific.pdf` (pp. 1–18; acciones por posición); `ijerph-17-09396.pdf` (pp. 1–15; relación pasador-receptor).

**Contenido:** principios ofensivos/defensivos y diferencias por grupos etarios o posición; movilidad, cobertura, unidad ofensiva; manipulación del espacio de interacción en tareas 10v9; relaciones espaciales y sincronía de subgrupos; acciones clave por posición desde perspectivas de entrenadores; coordinación entre pasador y receptor. Algunas fuentes se basan en muestras juveniles, ejercicios reducidos o percepciones de entrenadores y no sustentan reglas universales para fútbol profesional.

**Preguntas viables:**
- **Definición:** ¿Qué significan los principios de cobertura y movilidad en los estudios de acciones tácticas?
- **Comparación:** ¿Qué diferencias por posición se reportan en eficiencia táctica de jugadores juveniles?
- **Explicación:** ¿Cómo cambia el comportamiento colectivo cuando se manipula el espacio de interacción en una tarea 10v9?

### 9. Decisiones de entrenadores, análisis del rival y gestión del partido

**Fuentes principales:** `elstak-et-al-2025-naturalistic-decision-making-of-football-coaches.pdf` (pp. 1–13); `40721-Article Text-76355-1-10-20250903.pdf` (pp. 1–13); `fpsyg-13-914915.pdf` (pp. 1–11); `contexto_estilos.pdf` (pp. 1–22); `tt_systems_of_play.pdf` (pp. 1–2).

**Contenido:** señales y factores contextuales que intervienen en decisiones de entrenadores de alto nivel durante momentos dinámicos; propuesta práctica informada por teoría de juegos para análisis del rival en tiempo real; cambios de formación y desempeño; selección de sistemas considerando personal, rival, marcador, tiempo y condiciones. La evidencia disponible es principalmente descriptiva/conceptual para decisiones; no permite afirmar que una regla táctica produzca siempre mejores resultados.

**Preguntas viables:**
- **Definición:** ¿Qué señales del contexto consideran los entrenadores al decidir durante un partido?
- **Explicación:** ¿Cómo propone el artículo de análisis en tiempo real integrar el comportamiento del rival y la toma de decisiones?
- **Síntesis:** ¿Qué factores deberían contextualizar una decisión de cambiar de formación según las fuentes?

### 10. Análisis de rendimiento, tracking, redes, IA y entrenamiento

**Fuentes principales:** `fspor-07-1569155.pdf` (pp. 1–23; revisión sistemática de IA/dinámica táctica); `s40064-016-3108-2.pdf` (pp. 1–13; big data y análisis táctico); `decroos-kdd18.pdf` (pp. 1–10; descubrimiento automático de tácticas); `sensors-23-00273.pdf` (pp. 1–12; tracking y diagramas de Voronoi); `fpsyg-09-01900.pdf` e `ijerph-17-06649.pdf` (redes de pase/revisiones); `17479541221075734.pdf` (tracking defensivo); `sports-13-00244.pdf` (pp. 1–48; carga, conducta técnico-táctica y bienestar).

**Contenido:** datos de eventos y posicionamiento, redes de pase, métricas espaciales, diagramas de Voronoi, aprendizaje automático y descubrimiento de patrones; beneficios y problemas de validez/interpretación de indicadores; revisión de estudios sobre carga de entrenamiento, conducta técnico-táctica y bienestar. Estas fuentes sirven para preguntas sobre métodos, variables y límites de medición, no siempre para recomendar una táctica de partido.

**Preguntas viables:**
- **Definición:** ¿Qué diferencia hay entre datos de eventos y datos de tracking para describir el juego colectivo?
- **Comparación:** ¿Qué representa una red de pases y qué añade una medida espacial como Voronoi?
- **Limitaciones/síntesis:** ¿Qué límites recurrentes de medición y diseño señalan las revisiones de análisis táctico y carga de entrenamiento?

## Banco inicial de 30 preguntas justificables

Las preguntas anteriores suman 30 propuestas en niveles distintos. Este banco se puede usar como punto de partida y balancear por dificultad, temas y tipos de operación cognitiva: definiciones (10), explicaciones (9), comparaciones (6) y síntesis/limitaciones (5). Para la evaluación, conviene exigir que la respuesta cite documento y página y que distinga resultados observados de interpretaciones.

## Límites del corpus y temas que requieren cautela

- **Las transiciones no tienen una definición única en las fuentes.** La revisión `s12662-024-00951-9.pdf` expone diversidad de definiciones; una pregunta sólida debe especificar qué definición o fase usa.
- **Mecanismos causales de éxito ofensivo.** Algunas fuentes reportan asociaciones entre transiciones rápidas, remates/ocasiones y éxito; no todas demuestran por qué la relación ocurre. “Sorprender al rival” o “explotar su desorganización” debe presentarse como interpretación si el pasaje concreto no lo afirma.
- **Generalizaciones sobre formaciones.** Hay estudios observacionales, comparaciones de un experimento y marcos de identificación. No sostienen que una formación sea universalmente superior.
- **Eficacia comparada de presión/rest defence.** Las métricas difieren (recuperaciones, territorio, remates concedidos, compactación); no son intercambiables ni siempre se mide causalidad.
- **Saques de banda y algunos tipos de balón parado.** Hay estudios concretos, pero la revisión de balón parado señala evidencia desigual y escasa para determinados tipos de acción. Formular preguntas sobre el estudio, la muestra y el resultado medido, no reglas generales.
- **Decisiones y teoría de juegos.** El material ofrece marcos y análisis de práctica; hay poca evaluación causal de que un procedimiento de análisis mejore el resultado del partido.
- **Roles y principios por posición/edad.** Varias muestras son juveniles o recogen perspectivas de entrenadores; limitar las conclusiones a las poblaciones y contextos examinados.
- **Entrenamiento, carga y bienestar.** La revisión incluye estudios heterogéneos y observa que la integración de carga, conducta táctica y bienestar es limitada. No es una base suficiente para prescribir cargas individuales.
- **Ejemplos de sesión.** Los planes FIFA y otros documentos didácticos son útiles para preguntar por ejercicios, objetivos y consignas; no deben citarse como estudios empíricos de eficacia.
- **Calidad de extracción.** Hay artefactos OCR/PDF (ligaduras, palabras partidas por guion, tablas y símbolos) y metadatos incompletos en algunas filas. Para una pregunta basada en una cifra, tabla o cita, verificar el pasaje original del PDF. Los números de página aquí son páginas del PDF extraído.
- **Contenido periférico o limitado.** El documento `pone.0271093.pdf` trata liderazgo en varios códigos de fútbol y su transferencia al fútbol asociación es limitada; `pone.0243287.pdf` estudia visión del portero en tiros libres con una situación experimental específica; `sports-13-00244.pdf` trata carga y bienestar más que principios tácticos; `sensors-23-00273.pdf` aporta análisis espacial, no una explicación táctica completa.

## Recomendación para seleccionar las 30 preguntas finales

Priorizar las preguntas que exigen explicar un concepto o comparar dos fuentes con medidas compatibles; asignar referencias de respuesta esperada (archivo y página); incluir al menos una pregunta de límites metodológicos por tema empírico; y excluir preguntas que solo puedan responderse por conocimiento futbolístico general o por inferencias causales que los documentos no sostengan.
