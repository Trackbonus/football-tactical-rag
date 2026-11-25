# Ground truth para evaluar el Mini-RAG de táctica de fútbol

## Convención de identificación

`chunks_semanticos.json` contiene 5.487 objetos con `text`, `source` y `page`, pero no un campo ID. Para reproducibilidad, `chunk-NNNNN` representa el índice **1-based** en el arreglo JSON. La página es la asignada durante la extracción PDF. Los extractos son breves pasajes literales de los chunks, con saltos de línea normalizados. Solo se incluyen pasajes que aportan evidencia directa; compartir vocabulario no basta. “Explícito” es una afirmación del texto; “inferencia” es una síntesis prudente. Las asociaciones empíricas no implican causalidad universal.

## 1. ¿Qué es la contrapresión en el fútbol?

**Estado: verificable**

**Respuesta esperada.** Es el intento de recuperar inmediatamente el balón después de perderlo. En los estudios citados se delimita al sector ofensivo/tercio final y se trata como distinta de la presión tradicional.

**Ideas fundamentales esperadas.** Pérdida como disparador; intento inmediato de recuperación; mencionar que el criterio espacial corresponde a los estudios y no necesariamente a una definición universal.

| Chunk ID    | Documento                    | Página | Extracto                                                                                                                | Justificación                             |
| ----------- | ---------------------------- | -----: | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| chunk-00017 | `10.1515_jqas-2026-0001.pdf` |      2 | “a type of press where a team attempts to regain possession immediately after losing possession in the offensive zone.” | Define disparador y ubicación.            |
| chunk-00054 | `10.1515_jqas-2026-0001.pdf` |      7 | “immediately tries to regain possession … in the final third after losing it.”                                          | Reitera la definición del estudio.        |
| chunk-00018 | `10.1515_jqas-2026-0001.pdf` |      2 | “Gegenpressing is less structured … primary objective is to recover the ball without regard to positioning.”            | Aporta contraste con presión tradicional. |

**Observaciones o limitaciones.** No confundir contrapresión con toda presión alta: aquella parte de una pérdida reciente.

## 2. ¿Cuáles son las principales características tácticas de los sistemas 4-3-3 y 3-5-2?

**Estado: parcialmente verificable**

**Respuesta esperada.** El sistema 4-3-3 se organiza nominalmente con cuatro defensores, tres mediocampistas y tres delanteros. Sin embargo, la evidencia disponible solo confirma su utilización como formación en una tarea experimental, por lo que no permite describir exhaustivamente sus características tácticas. En cuanto al 3-5-2, el experimento analizado distribuyó sus cinco mediocampistas entre uno defensivo, dos ofensivos y otros dos jugadores. Además, se observó una disposición espacial más alargada en comparación con el 4-2-3-1, según la relación entre longitud y anchura del equipo. Estos resultados corresponden a condiciones experimentales específicas y no deben generalizarse automáticamente a otros contextos futbolísticos.

**Ideas fundamentales esperadas.**

- Reconocer la estructura nominal del 4-3-3 y del 3-5-2.
- Identificar la distribución específica de los mediocampistas del 3-5-2 observada en el experimento.
- Reconocer que el estudio encontró una disposición espacial más alargada del 3-5-2 respecto del 4-2-3-1, sin interpretar este resultado como una comparación directa entre el 4-3-3 y el 3-5-2.
- Diferenciar los resultados experimentales de las características tácticas generales de cada formación.
- No atribuir funciones, ventajas o comportamientos tácticos que no estén respaldados por la documentación.

| Chunk ID      | Documento                       | Página | Extracto                                                                                                                                              | Justificación                                                                                                                                                                                                      |
| ------------- | ------------------------------- | -----: | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `chunk-02081` | `FIFA_Session_Plan_Skinner.pdf` |      7 | “Set 1 team up in a 4-3-3 formation”                                                                                                                  | Confirma la utilización del 4-3-3 en una tarea experimental, pero no describe sus principios tácticos.                                                                                                             |
| `chunk-03833` | `pone.0210191.pdf`              |      4 | “five midfielders in the 3-5-2 formation were positioned as one defensive midfielder, two attacking midfielders and two”                              | Describe una distribución específica de los cinco mediocampistas del 3-5-2 en el experimento. El extracto disponible está incompleto, por lo que no permite identificar la función de los dos jugadores restantes. |
| `chunk-03861` | `pone.0210191.pdf`              |      8 | “Yet, the Player Length per Width ratio in the 3-5-2 formation exceeded the 4-2-3-1 formation, suggesting a more elongated player arrangement during” | Aporta un hallazgo experimental sobre la disposición espacial del 3-5-2. La comparación es con el 4-2-3-1, no con el 4-3-3.                                                                                        |
| `chunk-03862` | `pone.0210191.pdf`              |      8 | “careful not to generalize these results to elite soccer”                                                                                             | Advierte que los resultados experimentales no deben generalizarse automáticamente al fútbol de élite. Funciona como limitación metodológica, no como evidencia directa de las características de las formaciones.  |

**Observaciones o limitaciones.** La documentación disponible no permite construir un perfil táctico completo de ambos sistemas ni compararlos directamente en las mismas condiciones. Para el 4-3-3, solo se confirma su utilización en una tarea experimental. Para el 3-5-2, se dispone de información sobre una distribución específica de sus mediocampistas y sobre una variable de organización espacial comparada con el 4-2-3-1. Esta última comparación se conserva porque forma parte del hallazgo del estudio, pero no debe confundirse con una comparación directa entre las dos formaciones de la pregunta. Además, el extracto de `chunk-03833` está incompleto y no permite determinar la función de los dos mediocampistas restantes.

## 3. ¿Cómo se define una ocasión de gol?

**Estado: verificable**

**Respuesta esperada.** El documento `ocasiones_de_gol.pdf` define una ocasión de gol como una situación en la que el equipo observado tiene una clara oportunidad de marcar durante una posesión. Esto incluye tiros o posibilidades de tiro en las que el jugador está de cara a portería, tiene el balón controlado, no tiene oponentes entre el balón y la portería, y dispone de suficiente tiempo y espacio para tomar una decisión deliberada. Estas situaciones deben producirse dentro del pentágono de finalización. También se consideran ocasiones de gol los tiros realizados desde fuera de esa zona que pasan a menos de dos metros de la portería. Los goles están incluidos dentro de las ocasiones de gol.

**Ideas fundamentales esperadas.**

- Identificar la definición explícita de ocasión de gol proporcionada por el documento.
- Reconocer las condiciones exigidas para los tiros o posibilidades de tiro: orientación del jugador, control del balón, ausencia de oponentes entre el balón y la portería, y disponibilidad de tiempo y espacio para decidir.
- Distinguir las situaciones que ocurren dentro del pentágono de finalización de los tiros realizados desde fuera de este.
- Señalar que los goles están incluidos dentro de las ocasiones de gol.
- Aclarar que se trata de la definición operacional utilizada en el estudio, no necesariamente de una definición universal.

| Chunk ID      | Documento              | Página | Extracto                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Justificación                                                                                                                      |
| ------------- | ---------------------- | -----: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `chunk-03489` | `ocasiones_de_gol.pdf` |      3 | “Se considera ocasión de gol cuando el equipo observado tiene una clara oportunidad de marcar gol durante la posesión. Esto incluye todos los tiros o posibilidades de tiro (a- Jugador de cara a portería, b- con balón controlado, c- sin oponentes entre el balón y la portería y d- con suficiente tiempo y espacio para tomar una decisión deliberada) que tienen lugar dentro del pentágono de finalización (Figura 1). También son consideradas ocasión de gol aquellos tiros desde fuera del pentágono de finalización que pasan a una distancia menor a 2 metros respecto a la portería. Los goles están incluidos dentro de ocasión de gol.” | Evidencia principal: contiene la definición operacional y los criterios utilizados para identificar una ocasión de gol.            |
| `chunk-03481` | `ocasiones_de_gol.pdf` |      2 | “Además, estos autores argumentaron que las ocasiones de gol representan una evaluación multidimensional del escenario donde tiene lugar el intento de anotar, lo que puede aportar una más refinada medida que simplemente el hecho de contar el número de tiros producidos por un equipo.”                                                                                                                                                                                                                                                                                                                                                           | Contexto complementario: explica por qué las ocasiones de gol representan una medida más completa que el simple recuento de tiros. |
| `chunk-03480` | `ocasiones_de_gol.pdf` |      2 | “De esta manera, estudiar las ocasiones de gol como indicador de éxito ofrece un mayor contenido táctico para analizar y aporta un mejor entendimiento de como los goles pueden ser conseguidos.”                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Contexto complementario: describe la utilidad de estudiar las ocasiones de gol como indicador de éxito y análisis táctico.         |

**Observaciones o limitaciones.** La definición operacional corresponde al criterio utilizado en el estudio citado y no debe presentarse como una definición universal aplicable a todos los contextos del fútbol. El `chunk-03489` constituye la evidencia directa para responder la pregunta; los otros dos fragmentos aportan contexto, pero no son necesarios para establecer los criterios de identificación.

## 4. ¿Qué es la movilidad como principio táctico?

**Estado: verificable**

**Respuesta esperada.** _Depth mobility_ es el movimiento de jugadores en el espacio entre la última línea defensiva y la línea de gol. En FUT-SAT se clasifica como principio ofensivo.

**Ideas fundamentales esperadas.** Movimiento de jugadores sin balón en profundidad; espacio entre última línea y gol; diferenciarlo de la penetración del portador.

| Chunk ID    | Documento                  | Página | Extracto                                                                            | Justificación                 |
| ----------- | -------------------------- | -----: | ----------------------------------------------------------------------------------- | ----------------------------- |
| chunk-03209 | `hukin-58-207.pdf`         |      3 | “Depth Mobility — Movement of the players between the final defender and goal line” | Definición explícita.         |
| chunk-04273 | `rechenchoskyetal2017.pdf` |      4 | “Depth mobility — Movement of the players between the final defender and goal line” | Reproduce definición FUT-SAT. |

**Observaciones o limitaciones.** El término aparece como movilidad en profundidad; “movilidad” puede tener otros usos.

## 5. ¿Cómo cambian las formaciones de un equipo según la fase del juego?

**Estado: verificable**

**Respuesta esperada.** Las formaciones varían a lo largo del partido según el objetivo inmediato y la fase. Bauer et al. clasifica segmentos de juego en fases ofensivas y defensivas, y mide formaciones por separado en cada fase (por ejemplo, construcción, ataque, bloque alto, medio o bajo), evitando combinar todos los datos posicionales del partido en una única formación.

**Ideas fundamentales esperadas.** Cambio asociado a objetivos inmediatos; fases ofensivas y defensivas diferenciadas; medición contextualizada por fase; recordar que no todas las fases tienen datos suficientes para estimar una formación.

| Chunk ID    | Documento                                                                           | Página | Extracto                                                                                                                              | Justificación                                               |
| ----------- | ----------------------------------------------------------------------------------- | -----: | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| chunk-01134 | `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf` |      1 | “Teams change formation dynamically throughout matches to achieve their immediate”                                                    | Afirma cambios durante el encuentro vinculados a objetivos. |
| chunk-01135 | `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf` |      1 | “classify these segments into phases with an average F1-score of 0.76. We then measure and”                                           | Resume el procedimiento por fase.                           |
| chunk-01195 | `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf` |      8 | “teams defending strategy (high-/mid-/low-block). 4.2. Measuring formation in distinct phases of”                                     | Da ejemplos de fases/estrategias defensivas distintas.      |
| chunk-01197 | `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf` |      8 | “we aggregate together all the tracking data frames classiﬁed to a particular phase during the match and use them to measure the for” | Explica cómo se estima la formación condicionada por fase.  |

**Observaciones o limitaciones.** El método requiere observaciones suficientes por fase (el estudio indica un mínimo agregado de 60 segundos); no implica que cada equipo use siempre una formación distinta en cada fase.

## 6. ¿Qué factores se asocian con el éxito de un saque de esquina?

**Estado: verificable**

**Respuesta esperada.** La revisión incluida reporta asociaciones entre resultados de córneres y factores de ejecución/organización, como número y organización de atacantes y defensores, zona y tipo de envío, movimientos ofensivos, momento del partido, marcador, localía y ranking del rival. En un análisis resumido, 3?4 atacantes y un envío al segundo palo se asociaron con una mayor probabilidad de tiro bajo una configuración descrita. Son asociaciones de estudios concretos.

**Ideas fundamentales esperadas.** Mencionar variables de ejecución y organización; distinguir resultado de tiro de resultado de gol; presentar asociaciones contextualizadas y no como receta universal ni causalidad probada.

| Chunk ID    | Documento              | Página | Extracto                                                                                                                                   | Justificación                                               |
| ----------- | ---------------------- | -----: | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| chunk-00823 | `applsci-15-04984.pdf` |      2 | “delivery type (inswinging or outswinging) [5,7,17], delivery zone [5,7,18], and the number and organization of at- tacking and defending” | Enumera dimensiones técnico-tácticas examinadas.            |
| chunk-00849 | `applsci-15-04984.pdf` |      8 | “The likelihood of a shot from a corner increased significantly when 3–4 attackers were involved, especially with delivery toward”         | Asociaci?n concreta con producción de un tiro.              |
| chunk-00856 | `applsci-15-04984.pdf` |     10 | “influenced by match location, timing, scoreline, and opponent ranking”                                                                    | Factores contextuales asociados al éxito según la revisión. |
| chunk-00844 | `applsci-15-04984.pdf` |      7 | “Goals were linked to later match timing, dynamic offensive organization, 3–4 intervening attackers, and”                                  | Reporta variables asociadas a gol en estudios resumidos.    |

**Observaciones o limitaciones.** Es una revisión de estudios heterogéneos. “éxito” puede operacionalizarse como tiro, tiro entre palos o gol; la frecuencia de gol en córneres es baja y los hallazgos no garantizan resultados.

## 7. ¿Qué factores pueden influir en la generación de ocasiones de gol?

**Estado: verificable**

**Respuesta esperada.** Se estudian como factores asociados la zona inicial, posición/presión rival y amplitud de posesión; estado del marcador y calidad del equipo; y, en córneres, número de atacantes, movimientos dinámicos y zona/forma de envío. Los pases progresivos hacia fase final se asociaron con resultados positivos, incluidas ocasiones críticas y goles. Son resultados de estudios concretos, no causalidad universal.

**Ideas fundamentales esperadas.** Factores tácticos y contextuales; variables propias de balón parado; hablar de asociación y no de garantía causal.

| Chunk ID    | Documento                                                                                                                   | Página | Extracto                                                                                                                                                         | Justificación                                           |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- | -----: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| chunk-02698 | `fspor-06-1473311.pdf`                                                                                                      |      2 | “Therefore, the aim of this study was to evaluate the effect of contextual and tactical dimensions on the offensive performance”                                 | Enumera factores examinados en ataques directos.        |
| chunk-02689 | `fspor-06-1473311.pdf`                                                                                                      |      1 | “only “Width of the possession” showed association with “Scoring opportunity performance” (p < 0.01). Two of the four contextual dimensions (“Match status” and” | Precisa resultado para creación de ocasiones.           |
| chunk-00900 | `applsci-15-04984.pdf`                                                                                                      |     17 | “3–4 actively involved players … dynamic movements … likelihood of creating goal-scoring”                                                                        | Síntesis de factores en córner ofensivo.                |
| chunk-01628 | `deb-et-al-2024-creating-an-augmented-possession-framework-to-evaluate-phases-of-play-and-application-in-international.pdf` |      1 | “Progressive passing showed increased odds of positive phase outcomes when attempting to enter the”                                                              | Relaciona pase progresivo con resultados de fase final. |

**Observaciones o limitaciones.** Los factores y resultados dependen de muestra, operacionalización y contexto de cada estudio.

## 8. ¿Qué características de los saques de banda pueden influir en conservar el balón?

**Estado: verificable**

**Respuesta esperada.** En el estudio incluido, ejecutar rápido, sin presión rival y hacia atrás se asoció con menor pérdida; los saques largos y medianos se asociaron con más pérdidas que los cortos. También importó la zona. El saque corto hacia atrás puede conservar posesión, pero reducir la opción de producir un intento o gol.

**Ideas fundamentales esperadas.** Rapidez, presión, dirección, longitud y zona; distinguir conservar balón de progresar o finalizar.

| Chunk ID    | Documento          | Página | Extracto                                                                                                                           | Justificación                              |
| ----------- | ------------------ | -----: | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| chunk-04097 | `pone.0294317.pdf` |      8 | “Fast throw-ins decreased the odds of losing possession by 24.5% (OR = 0.755) in favor of continuing possession, compared to slow” | Variables asociadas a pérdida/continuidad. |
| chunk-04101 | `pone.0294317.pdf` |     10 | “Throw-ins executed from the defensive zone … higher probability of lost possession”                                               | Evidencia sobre zona.                      |
| chunk-04114 | `pone.0294317.pdf` |     11 | “short backwards throw-ins allow us to ensure possession of the ball, but, nevertheless, they decrease our chances of achieving”   | Aclara el costo ofensivo posible.          |

**Observaciones o limitaciones.** Resultados observacionales de una muestra concreta; mantener lenguaje asociativo.

## 9. ¿Cómo se identifican las formaciones a partir de la posición de los jugadores?

**Estado: verificable**

**Respuesta esperada.** Se utilizan datos posicionales y se contextualizan por fase de juego. Bauer et al. clasifica las fases a lo largo del encuentro y agrega los periodos de una misma fase para medir las formaciones, evitando mezclar todas las posiciones del partido en una sola configuración estática.

**Ideas fundamentales esperadas.** Datos de seguimiento; clasificación temporal de fases; agregación de configuraciones por fase; contemplar cambios durante el partido.

| Chunk ID    | Documento                                                                           | Página | Extracto                                                                              | Justificación                           |
| ----------- | ----------------------------------------------------------------------------------- | -----: | ------------------------------------------------------------------------------------- | --------------------------------------- |
| chunk-01159 | `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf` |      3 | “classify a football match over time into distinct phases … before measuring the”     | Secuencia del método.                   |
| chunk-01160 | `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf` |      3 | “periods … same phases … aggregated to obtain precise measurements of the formations” | Explica medición contextualizada.       |
| chunk-01190 | `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf` |      7 | “aggregate player positions over the entire match ignoring tactical changes”          | Expone limitación de enfoque estático.  |
| chunk-01186 | `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf` |      7 | “first 6 seconds after a team gains ball possession are classified as transition to”  | Ejemplo de delimitación de fase previa. |

**Observaciones o limitaciones.** No implica que la formación pueda identificarse con certeza a partir de una imagen aislada.

## 10. ¿Cómo se pueden entrenar los contraataques?

**Estado: verificable**

**Respuesta esperada.** El plan de sesión FIFA propone preparación cognitiva, pases al espacio y desmarques, juego reducido con transición inmediata tras recuperar el balón y un ejercicio desde bloque bajo. Sus consignas incluyen rapidez, comunicación, primer pase preciso, amplitud/profundidad, carreras diagonales, avance colectivo y jugar fuera de la presión hacia espacios libres.

**Ideas fundamentales esperadas.** Simular pérdida/recuperación; entrenar pases y desmarques; rapidez de decisión y coordinación; progresar a bloque bajo.

| Chunk ID    | Documento                             | Página | Extracto                                                                                                           | Justificación                            |
| ----------- | ------------------------------------- | -----: | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| chunk-02085 | `FIFA_Session_Plan_Urias_counter.pdf` |      1 | “Cognitive preparation … passing and running in behind … 3v3 into a counter-attack … counter-attacking from a low” | Progresión de actividades.               |
| chunk-02089 | `FIFA_Session_Plan_Urias_counter.pdf` |      1 | “move quickly, communication … first pass is accurate, creating width and depth, making diagonal”                  | Principios de entrenamiento mencionados. |
| chunk-02101 | `FIFA_Session_Plan_Urias_counter.pdf` |      4 | “Immediately after winning the ball back … launch a counter-attack”                                                | Entrena transición inmediata.            |
| chunk-02103 | `FIFA_Session_Plan_Urias_counter.pdf` |      4 | “play the ball away from pressure and into space … passes between the gaps”                                        | Decisiones y ocupación del espacio.      |
| chunk-02108 | `FIFA_Session_Plan_Urias_counter.pdf` |      5 | “moving the ball away from pressure and into space … make runs in behind”                                          | Consignas desde bloque bajo.             |

**Observaciones o limitaciones.** Es material didáctico de sesión, no ensayo de eficacia competitiva.

## 11. ¿Qué aspectos se analizan en cada etapa de una posesión?

**Estado: verificable**

**Respuesta esperada.** El marco de Deb et al. separa 1.ª fase, 2.ª fase, fase final y transición de defensa a ataque. Considera ubicación del balón y forma de ambos equipos, progresión entre fases, acciones como pases/conducciones progresivas y resultados como progresión exitosa, posesión peligrosa, tiro, ocasión crítica, gol o pérdida.

**Ideas fundamentales esperadas.** Nombrar fases; posición y organización de equipos; acciones/progresión; resultados y riesgos diferenciados.

| Chunk ID    | Documento                                                                                                                   | Página | Extracto                                                                                            | Justificación                        |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- | -----: | --------------------------------------------------------------------------------------------------- | ------------------------------------ |
| chunk-01626 | `deb-et-al-2024-creating-an-augmented-possession-framework-to-evaluate-phases-of-play-and-application-in-international.pdf` |      1 | “1st Phase, 2nd Phase, Final Phase and Transition Defence to Attack”                                | Enumera etapas del marco.            |
| chunk-01650 | `deb-et-al-2024-creating-an-augmented-possession-framework-to-evaluate-phases-of-play-and-application-in-international.pdf` |      3 | “phases not only by the ball location … but also in context of the opposition shape”                | Dimensiones tácticas por fase.       |
| chunk-01642 | `deb-et-al-2024-creating-an-augmented-possession-framework-to-evaluate-phases-of-play-and-application-in-international.pdf` |      2 | “primary focus is to progress to the next phase, making progres- sion rates a key outcome measure.” | Objetivo de progresión.              |
| chunk-01643 | `deb-et-al-2024-creating-an-augmented-possession-framework-to-evaluate-phases-of-play-and-application-in-international.pdf` |      2 | “rate of turnover … likelihood of progressing … dangerous situations”                               | Riesgos y recompensas evaluados.     |
| chunk-01628 | `deb-et-al-2024-creating-an-augmented-possession-framework-to-evaluate-phases-of-play-and-application-in-international.pdf` |      1 | “Progressive passing showed increased odds of positive phase outcomes when attempting to enter the” | Resultados que distingue el estudio. |

**Observaciones o limitaciones.** Taxonomía específica del marco, no universal.

## 12. ¿En qué se diferencian el 4-2-3-1 y el 3-5-2?

**Estado: verificable**

**Respuesta esperada.** En el experimento citado, el 3-5-2 tuvo disposición atacante relativamente más alargada y mayor eficiencia de pase bajo presión; el 4-2-3-1 mostró forma más ancha. No hubo diferencia significativa en todas las métricas, por lo que no se concluye superioridad global.

**Ideas fundamentales esperadas.** Contraste espacial; resultados de longitud/anchura y pase bajo presión; cautela sobre alcance.

| Chunk ID    | Documento          | Página | Extracto                                                                                                                                              | Justificación                     |
| ----------- | ------------------ | -----: | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| chunk-03832 | `pone.0210191.pdf` |      3 | “more elongated attacking shape compared to the wider 4-2-3-1”                                                                                        | Diferencia espacial.              |
| chunk-03861 | `pone.0210191.pdf` |      8 | “Yet, the Player Length per Width ratio in the 3-5-2 formation exceeded the 4-2-3-1 formation, suggesting a more elongated player arrangement during” | Resume hallazgos.                 |
| chunk-03864 | `pone.0210191.pdf` |      8 | Ratio `0.64` vs. `0.59`; eficiencia de pase bajo presión `4.56` vs. `2.30`                                                                            | Tabla de comparación.             |
| chunk-03859 | `pone.0210191.pdf` |      8 | “3-5-2 … 4.56 … significantly higher … than … 4-2-3-1 … 2.3”                                                                                          | Resultado estadístico específico. |

**Observaciones o limitaciones.** Montaje experimental y medidas seleccionadas; no comparación exhaustiva de funciones o temporadas.

## 13. ¿En que se diferencian el estilo de juego del Barcelona y el Manchester City de Guardiola?

**Estado: parcialmente verificable**

**Respuesta esperada.** Ambos equipos se caracterizan por priorizar la posesión del balón y utilizar los pases para progresar y mantener el control del juego. Sin embargo, pueden presentar diferencias en la distribución espacial de los pases y en la manera de organizar la posesión. Estas diferencias dependen del equipo, el contexto y el periodo analizado, por lo que no corresponde establecer una superioridad general de uno sobre otro a partir de los datos disponibles.

**Ideas fundamentales esperadas.** Citar temporadas y tipos/niveles de pase; limitar el contraste a las variables estudiadas; no adjudicar diferencias al entrenador ni generalizar a otros periodos.

| Chunk ID    | Documento                                              | Página | Extracto                                                                                               | Justificación                                   |
| ----------- | ------------------------------------------------------ | -----: | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| chunk-04165 | `produccion_retos,+Retos+56+(179-187)+104182+esp..pdf` |      2 | “F.C. Barcelona 2011/2012 Número de secuencias ofensivas P”                                            | Delimita equipos y temporadas del estudio.      |
| chunk-04194 | `produccion_retos,+Retos+56+(179-187)+104182+esp..pdf` |      5 | “pases de conservación ( = 0.000) predominan en niveles bajos en el F.C. Barcelona y son ligeramente” | Comparaci?n directa de los indicadores de pase. |

**Observaciones o limitaciones.** Respaldo parcial para “estilo de juego”: se observan secuencias e indicadores específicos de dos temporadas. No se demuestra atribución a Guardiola ni se caracteriza el estilo completo de ambos equipos.

## 14. ¿Qué variables se relacionan con el rendimiento de los ataques directos?

**Estado: verificable**

**Respuesta esperada.** El estudio de ataques directos en partidos de La Liga y la Premier League analizó dimensiones tácticas y contextuales como zona inicial, posición y presión inicial del rival y amplitud de la posesión, usando como resultados el grado de penetración y la creación de ocasiones. En los resultados reportados, la amplitud de la posesión se asoci? con el rendimiento de creación de ocasiones. No se debe concluir que todas las variables examinadas mostraron asociación.

**Ideas fundamentales esperadas.** Identificar variables de contexto/acción; separar variables analizadas de las que mostraron asociación; mencionar que la evidencia procede de una muestra de ligas y partidos.

| Chunk ID    | Documento              | Página | Extracto                                                                                                                                                         | Justificación                                                 |
| ----------- | ---------------------- | -----: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| chunk-02698 | `fspor-06-1473311.pdf` |      2 | “Therefore, the aim of this study was to evaluate the effect of contextual and tactical dimensions on the offensive performance”                                 | Define alcance del estudio y resultados ofensivos observados. |
| chunk-02719 | `fspor-06-1473311.pdf` |      5 | “Initial zone” (0.952 and 0.945), “Initial opponent position” (0.940 and 0.911), “Initial”                                                                       | Enumera dimensiones operacionales.                            |
| chunk-02689 | `fspor-06-1473311.pdf` |      1 | “only “Width of the possession” showed association with “Scoring opportunity performance” (p < 0.01). Two of the four contextual dimensions (“Match status” and” | Precisa qué variable se asoci? con rendimiento de ocasión.    |

**Observaciones o limitaciones.** Estudio observacional de posesiones seleccionadas de La Liga y EPL; asociación no demuestra causalidad y los resultados dependen de las definiciones usadas.

## 15. ¿Qué diferencias existen entre un córner y un saque de banda?

**Estado: parcialmente verificable**

**Respuesta esperada.** El corpus los clasifica como tipos diferentes de balón parado. Para córneres, estudia factores de envío, organización ofensiva/defensiva y resultados como tiros o goles; para saques de banda, examina rapidez, presión, longitud, direcci?n y zona en relación con conservar o perder la posesión. No contiene suficiente evidencia reglamentaria para describir todas las diferencias de ejecución.

**Ideas fundamentales esperadas.** Son reinicios distintos; describir qué resultados y variables investigan las fuentes para cada uno; no añadir reglas que el corpus no documenta.

| Chunk ID    | Documento                                                                           | Página | Extracto                                                                                                                                   | Justificación                                                          |
| ----------- | ----------------------------------------------------------------------------------- | -----: | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| chunk-01171 | `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf` |      4 | “set-pieces providing a separate category (which could also be broken further down into offensive and defensive”                           | Los identifica como categorías distintas de balón parado.              |
| chunk-00823 | `applsci-15-04984.pdf`                                                              |      2 | “delivery type (inswinging or outswinging) [5,7,17], delivery zone [5,7,18], and the number and organization of at- tacking and defending” | Variables estudiadas en córneres.                                      |
| chunk-04097 | `pone.0294317.pdf`                                                                  |      8 | “Fast throw-ins decreased the odds of losing possession by 24.5% (OR = 0.755) in favor of continuing possession, compared to slow”         | Variables estudiadas en saques de banda y su relación con continuidad. |
| chunk-04114 | `pone.0294317.pdf`                                                                  |     11 | “short backwards throw-ins allow us to ensure possession of the ball, but, nevertheless, they decrease our chances of achieving”           | Explicita una posible diferencia entre conservar y producir ataque.    |

**Observaciones o limitaciones.** La comparación respaldada es de clasificación y de variables estudiadas, no una comparación normativa completa ni una evaluación directa entre ambos reinicios.

## 16. ¿En qué se diferencian la presión alta y la contrapresión?

**Estado: verificable**

**Respuesta esperada.** La presión alta presiona arriba al rival mientras este construye o tiene el balón. La contrapresión es la reacción inmediata tras perder la posesión propia. La diferencia central está en el momento/disparador; “alta” también alude a la zona.

**Ideas fundamentales esperadas.** Zona avanzada para presión alta; pérdida reciente para contrapresión; no confundir ubicación con transición.

| Chunk ID    | Documento                                    | Página | Extracto                                                                      | Justificación                               |
| ----------- | -------------------------------------------- | -----: | ----------------------------------------------------------------------------- | ------------------------------------------- |
| chunk-00017 | `10.1515_jqas-2026-0001.pdf`                 |      2 | “regain possession immediately after losing possession in the offensive zone” | Define contrapresión.                       |
| chunk-00054 | `10.1515_jqas-2026-0001.pdf`                 |      7 | “after losing it … final third”                                               | Reafirma momento/localización.              |
| chunk-00511 | `40721-Article Text-76355-1-10-20250903.pdf` |      6 | “high press while Team B attempts to build up from the back”                  | Ejemplo de presión alta contra salida.      |
| chunk-00989 | `Art+233.pdf`                                |      5 | “high pressure was applied slightly more often in the offensive zone”         | Evidencia contextual de presión adelantada. |

**Observaciones o limitaciones.** No se fija una altura métrica universal para “alta”.

## 17. ¿Por qué es difícil clasificar el estilo de juego de un equipo?

**Estado: verificable**

**Respuesta esperada.** La literatura usa terminologías, indicadores y escalas diferentes: algunos estilos describen al equipo globalmente y otros fases específicas; se apoyan en factores técnicos, tácticos o físicos; dependen de jugadores y de su selección; y se relacionan con contexto como marcador, localía, rival, liga, edad y superficie. Las categorías requieren definiciones y cautela al comparar estudios.

**Ideas fundamentales esperadas.** Heterogeneidad de taxonomías; diferentes fases/dimensiones; efecto de plantilla y contexto; cautela con categorías construidas.

| Chunk ID    | Documento                                                                                                   | Página | Extracto                                                                                          | Justificación                                |
| ----------- | ----------------------------------------------------------------------------------------------------------- | -----: | ------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| chunk-03579 | `plakias-et-al-2024-a-grounded-theory-for-professional-soccer-teams-playing-styles-towards-a-consensus.pdf` |      2 | “some … characterize some teams as a whole … [others] refer exclusively to specific”              | Variación de alcance del concepto.           |
| chunk-03580 | `plakias-et-al-2024-a-grounded-theory-for-professional-soccer-teams-playing-styles-towards-a-consensus.pdf` |      2 | “formations … match location, match status … country … league … age group … playing”              | Variables/contextos relacionados.            |
| chunk-03581 | mismo documento                                                                                             |      2 | “playing style may be determined by … players … [or] selection of players … based on the playing” | Relación entre plantilla y estilo.           |
| chunk-03606 | mismo documento                                                                                             |      5 | “84 codes … 6 folders … terms that the authors … used instead of … ‘playing style’”               | Señala diversidad de códigos y terminología. |

**Observaciones o limitaciones.** La revisión indica heterogeneidad; no que clasificar sea imposible.

## 18. ¿Cómo puede afectar la barrera la visión del portero ante un tiro libre?

**Estado: verificable**

**Respuesta esperada.** Si la barrera oculta inicialmente la trayectoria del balón, el portero recibe tarde información visual. En un simulador, la oclusión retrasó el inicio del movimiento y redujo el rendimiento al detener tiros libres. El estudio advierte límites de generalización a partidos reales.

**Ideas fundamentales esperadas.** Oclusión de trayectoria inicial; retraso de respuesta por menor información visual; peor rendimiento de atajada; limitaciones experimentales.

| Chunk ID    | Documento          | Página | Extracto                                                                                       | Justificación                        |
| ----------- | ------------------ | -----: | ---------------------------------------------------------------------------------------------- | ------------------------------------ |
| chunk-03902 | `pone.0243287.pdf` |      1 | “performance … reduces when the defensive wall blocks their initial view of the ball”          | Título resume la conclusión central. |
| chunk-03991 | `pone.0243287.pdf` |     13 | “Both groups … delayed their movement onset when the wall was present.”                        | Efecto conductual medido.            |
| chunk-04015 | `pone.0243287.pdf` |     16 | “visual occlusion of the initial ball trajectory by the wall … negatively affects goalkeeping” | Conclusión explícita.                |
| chunk-04001 | `pone.0243287.pdf` |     15 | “virtual reality goalkeeping simulator was realistic, some aspects differed from real”         | Sustenta cautela metodológica.       |

**Observaciones o limitaciones.** Evidencia de simulador y condiciones controladas; generalización a porteros expertos y partidos reales es limitada.

## 19. ¿Qué ventajas y limitaciones presentan los ataques directos frente a los ataques basados en la posesión?

**Estado: parcialmente verificable**

**Respuesta esperada.** El corpus incluye un estudio de ataques directos que analiza su penetración y creación de ocasiones según dimensiones tácticas/contextuales, y señala que un repertorio variado de tipos de ataque podría contribuir al rendimiento ofensivo. Sin embargo, los fragmentos disponibles no establecen una comparación empírica equilibrada de ventajas y limitaciones entre ataque directo y ataque basado en posesión. No corresponde afirmar cu?l es superior ni atribuir ventajas específicas a cada uno.

**Ideas fundamentales esperadas.** Informar qué analiza la fuente de ataque directo; declarar que falta evidencia comparativa suficiente para ambos estilos; no completar la respuesta con conocimientos externos.

| Chunk ID    | Documento              | Página | Extracto                                                                                                                                                         | Justificación                                                             |
| ----------- | ---------------------- | -----: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| chunk-02698 | `fspor-06-1473311.pdf` |      2 | “Therefore, the aim of this study was to evaluate the effect of contextual and tactical dimensions on the offensive performance”                                 | Respalda el análisis del ataque directo, no una comparación con posesión. |
| chunk-02689 | `fspor-06-1473311.pdf` |      1 | “only “Width of the possession” showed association with “Scoring opportunity performance” (p < 0.01). Two of the four contextual dimensions (“Match status” and” | Resultado dentro del análisis de ataques directos.                        |

**Observaciones o limitaciones.** No se localiz? evidencia directa que compare las ventajas y limitaciones de ambas modalidades en condiciones comunes. La pregunta requiere reconsideración o fuentes comparativas adicionales.

## 20. ¿Cómo pueden utilizarse las redes de pases para identificar la estructura y las relaciones entre jugadores de un equipo?

**Estado: verificable**

**Respuesta esperada.** En redes basadas en jugadores, estos se representan como nodos y los pases ponderados como conexiones; las métricas de red pueden mostrar patrones de interacción, roles importantes como el de organizador y coordinaci?n del equipo. Un análisis centrado solo en jugadores puede dejar fuera la ocupaci?n espacial del campo; las redes de pases por zonas complementan el análisis representando ?reas como nodos y pases entre zonas como conexiones.

**Ideas fundamentales esperadas.** Nodos y conexiones representan jugadores e interacciones por pase; métricas resumen estructura/roles; red de jugadores y red espacial responden preguntas relacionadas pero distintas; no asumir que una red prueba causalidad o revela por s? sola toda la táctica.

| Chunk ID    | Documento                     | Página | Extracto                                                                                                                          | Justificación                                               |
| ----------- | ----------------------------- | -----: | --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| chunk-00587 | `41598_2025_Article_4507.pdf` |      1 | “treating players as nodes and employing weighted passes”                                                                         | Define representaci?n de las interacciones entre jugadores. |
| chunk-00588 | `41598_2025_Article_4507.pdf` |      1 | “identified crucial roles, such as playmakers, and revealed team coordination strategies through network metrics, it often”       | Indica usos para roles y relaciones colectivas.             |
| chunk-00588 | `41598_2025_Article_4507.pdf` |      1 | “identified crucial roles, such as playmakers, and revealed team coordination strategies through network metrics, it often”       | Explica redes de pases espaciales como complemento.         |
| chunk-00589 | `41598_2025_Article_4507.pdf` |      1 | “This analytical framework offers significant advantages as it quantifies teams’ spatial control strategies, uncovers systematic” | Describe qué puede aportar el análisis espacial por zonas.  |

**Observaciones o limitaciones.** Las conclusiones dependen de cómo se construyan nodos, conexiones, pesos y métricas. La red no representa todos los movimientos sin balón ni prueba por s? sola mecanismos causales.

## 21. ¿Qué factores tácticos influyen en la eficacia ofensiva de los córners y tiros libres indirectos?

**Estado: verificable**

**Respuesta esperada.** En córneres, las fuentes revisadas asocian la producción de tiros con el número de atacantes y la zona de envío; también analizan el tipo de envío, la organización din?mica y la disposición defensiva. En tiros libres indirectos del Mundial 2014, se asociaron con resultados de eficacia la organización ofensiva din?mica, el número de atacantes que intervienen, el trayecto a?reo del balón y el número de defensores, aunque los predictores varían según se mida tiro, tiro entre palos o gol.

**Ideas fundamentales esperadas.** Tratar córner y tiro libre indirecto como situaciones distintas; mencionar organización/movimiento, atacantes y envío/defensa; distinguir resultados y no presentar asociaciones como causalidad general.

| Chunk ID    | Documento              | Página | Extracto                                                                                                                                   | Justificación                                                             |
| ----------- | ---------------------- | -----: | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| chunk-00849 | `applsci-15-04984.pdf` |      8 | “The likelihood of a shot from a corner increased significantly when 3–4 attackers were involved, especially with delivery toward”         | Hallazgo táctico para córneres sobre tiros.                               |
| chunk-00823 | `applsci-15-04984.pdf` |      2 | “delivery type (inswinging or outswinging) [5,7,17], delivery zone [5,7,18], and the number and organization of at- tacking and defending” | Enumera variables tácticas estudiadas en córneres.                        |
| chunk-00237 | `16752019005.pdf`      |      6 | “five variables that were significantly associated with shot. These were Number of defenders (χ2 = 7.63, p = .02), Deliv”                  | Enumera asociaciones para el criterio de tiro en tiros libres indirectos. |
| chunk-00245 | `16752019005.pdf`      |      7 | “For the criterion shot (Table 5), the probability of a suc- cessful outcome was 10.055 higher when the indirect free kick was”            | Resume resultados de regresi?n para tiros libres indirectos.              |

**Observaciones o limitaciones.** El estudio de tiros libres indirectos codifica por separado tiro, tiro entre palos y gol y analiza 506 acciones de un torneo (Mundial 2014). Para córneres, la revisión re?ne estudios con muestras y criterios heterogéneos. Los factores no constituyen una receta universal.

## 22. ¿Cómo puede influir la calidad del rival en el comportamiento táctico y espacial de un equipo?

**Estado: verificable**

**Respuesta esperada.** La calidad de los equipos puede relacionarse con diferencias en su comportamiento táctico y espacial durante los partidos. Sin embargo, la evidencia disponible se refiere a la calidad del equipo en general y no permite atribuir directamente esas diferencias a la calidad del rival. Por tanto, no se puede establecer una relación específica entre la calidad del oponente y los cambios tácticos o espaciales sin evidencia adicional.

**Ideas fundamentales esperadas.** La calidad del rival es una variable contextual; puede asociarse con estilos, posesión, zona de recuperaci?n y ubicaci?n de línea defensiva; distinguir resultados de distintos estudios y no universalizarlos.

| Chunk ID    | Documento                     | Página | Extracto                                                                                                                                         | Justificación                                                                                                  |
| ----------- | ----------------------------- | -----: | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| chunk-01324 | `contexto_estilos.pdf`        |      2 | “The aim of the present study was to evaluate the effect of match status, venue, 2 and quality of opposition on the styles of”                   | Sit?a la calidad del rival entre las variables estudiadas.                                                     |
| chunk-01325 | `contexto_estilos.pdf`        |      2 | “except Counterattack and Maintenance, and quality of 10 opposition had a significant”                                                           | Resultado específico sobre estilos.                                                                            |
| chunk-01333 | `contexto_estilos.pdf`        |      4 | “defensive line are closer to a team’s own goal when the opposition is stronger 9 (Santos et al., 2017). Hence, quality of opposition seemed to” | Evidencia espacial reportada en un estudio de caso citado.                                                     |
| chunk-00591 | `41598_2025_Article_4507.pdf` |      1 | “team quality influences tactical approaches and spatial control capabilities”                                                                   | Conecta calidad del equipo/rival con enfoques tácticos y control espacial en la revisión del estudio de redes. |

**Observaciones o limitaciones.** Se combinan análisis con dise?os y operacionalizaciones diferentes; el pasaje sobre línea defensiva resume un estudio de caso. ?Influir? debe expresarse como asociación contextual, no como efecto universal o causal demostrado.

## Resumen de cobertura

- **Verificables:** 17 (1, 4–12, 14, 16–18 y 20–22).
- **Parcialmente verificables:** 5 (2, 3, 13, 15 y 19).
- **Sin respaldo suficiente:** 0.

La pregunta **19** requiere reconsideración: el corpus no sustenta una comparación directa de ventajas y limitaciones entre ataques directos y ataques basados en la posesión. Las preguntas parcialmente verificables deben responderse explicitando el alcance y los vacíos documentados en cada secci?n.

## Documentos citados con mayor frecuencia

Conteo actualizado automáticamente a partir de las filas de evidencia de las 22 preguntas. Las repeticiones entre preguntas se cuentan por separado.

| Documento                                                                                                                   | Apariciones |
| --------------------------------------------------------------------------------------------------------------------------- | ----------: |
| `bauer-et-al-2023-putting-team-formations-in-association-football-into-context.pdf`                                         |          10 |
| `deb-et-al-2024-creating-an-augmented-possession-framework-to-evaluate-phases-of-play-and-application-in-international.pdf` |           8 |
| `applsci-15-04984.pdf`                                                                                                      |           8 |
| `pone.0210191.pdf`                                                                                                          |           7 |
| `fspor-06-1473311.pdf`                                                                                                      |           7 |
| `10.1515_jqas-2026-0001.pdf`                                                                                                |           5 |
| `pone.0294317.pdf`                                                                                                          |           5 |
| `FIFA_Session_Plan_Urias_counter.pdf`                                                                                       |           5 |
| `41598_2025_Article_4507.pdf`                                                                                               |           5 |
| `pone.0243287.pdf`                                                                                                          |           4 |
| `contexto_estilos.pdf`                                                                                                      |           3 |
| `produccion_retos,+Retos+56+(179-187)+104182+esp..pdf`                                                                      |           2 |
| `plakias-et-al-2024-a-grounded-theory-for-professional-soccer-teams-playing-styles-towards-a-consensus.pdf`                 |           2 |
| `16752019005.pdf`                                                                                                           |           2 |
| `FIFA_Session_Plan_Skinner.pdf`                                                                                             |           1 |
| `hukin-58-207.pdf`                                                                                                          |           1 |
| `rechenchoskyetal2017.pdf`                                                                                                  |           1 |
| `40721-Article Text-76355-1-10-20250903.pdf`                                                                                |           1 |
| `Art+233.pdf`                                                                                                               |           1 |

## Cautelas de uso

Los chunks pueden contener cortes de frase y artefactos de extracción. Los IDs son índices del archivo actual, no IDs persistentes del esquema. Verificar en el PDF las cifras o definiciones decisivas. Esta referencia no completa vacíos con conocimiento futbolístico externo ni convierte asociaciones en causalidad.
