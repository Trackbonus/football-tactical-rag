# Mini-RAG de táctica de fútbol

Sistema de recuperación aumentada por generación (RAG) orientado a responder preguntas sobre conceptos tácticos del fútbol a partir de un corpus de documentos especializados.

El proyecto implementa un pipeline local de procesamiento de documentos, fragmentación, generación de embeddings, recuperación de información, re-ranking y generación de respuestas mediante modelos ejecutados con Ollama.

## Características principales

- Extracción de texto desde documentos PDF.
- Fragmentación fija y semántica.
- Generación de embeddings mediante Ollama.
- Recuperación basada en embeddings, TF-IDF o un enfoque híbrido.
- Recuperación híbrida que combina embeddings y BM25.
- Reordenamiento de candidatos mediante CrossEncoder.
- Expansión de candidatos considerando documentos de origen.
- Generación de respuestas fundamentadas en los fragmentos recuperados.
- Evaluación mediante preguntas, ground truth y métricas de recuperación y calidad de respuesta.

## Tecnologías y modelos

- Python.
- Ollama.
- NumPy y SciPy.
- scikit-learn.
- PyMuPDF y PyMuPDF4LLM.
- Sentence Transformers.

Modelos utilizados:

| Componente               | Modelo                                       |
| ------------------------ | -------------------------------------------- |
| Generación de respuestas | `gemma3:4b`                                  |
| Embeddings               | `embeddinggemma`                             |
| Re-ranking               | `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` |

## Estructura del proyecto

```text
football-tactical-rag/
├── main.py
├── generate_baseline.py
├── requirements.txt
├── README.md
├── .gitignore
├── baseline/
├── documentos/
├── evaluacion/
└── resultados/
```

- `main.py`: implementación principal del Mini-RAG.
- `generate_baseline.py`: generación de la línea base.
- `baseline/`: implementación y respuesta de referencia.
- `documentos/`: corpus documental utilizado.
- `evaluacion/`: preguntas, respuestas y evaluación completa.
- `resultados/`: fragmentos semánticos, ground truth y resumen del corpus.

## Requisitos

- Python compatible con las dependencias de `requirements.txt`.
- Ollama instalado y en ejecución.
- Modelos locales descargados mediante Ollama.

Descargar los modelos:

```bash
ollama pull gemma3:4b
ollama pull embeddinggemma
```

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Trackbonus/football-tactical-rag.git
cd football-tactical-rag
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Verificar que Ollama esté ejecutándose y que los modelos necesarios estén disponibles.

Iniciar el sistema:

```bash
python main.py
```

El programa procesa el corpus documental, genera o reutiliza los embeddings y permite realizar preguntas sobre táctica de fútbol desde la terminal.

## Configuración

La estrategia de fragmentación puede seleccionarse mediante la variable de entorno `CHUNKING_STRATEGY`:

- `semantic`: fragmentación semántica (valor predeterminado).
- `fixed`: fragmentación de tamaño fijo.

En PowerShell:

```powershell
$env:CHUNKING_STRATEGY="semantic"
python main.py
```

## Evaluación

La carpeta `evaluacion/` contiene las preguntas y respuestas utilizadas durante las pruebas, además del documento de evaluación completa.

La carpeta `resultados/` contiene:

- `chunks_semanticos.json`: fragmentos generados a partir del corpus.
- `ground_truth_evaluacion.md`: referencias utilizadas para evaluar la recuperación.
- `resumen_corpus_evaluacion.md`: descripción del corpus y sus características.

Las métricas consideradas incluyen Recall@4, MRR@4, faithfulness, relevancia y exactitud.

## Consideraciones

- La generación de respuestas y embeddings se realiza localmente mediante Ollama.
- La primera ejecución puede tardar debido al procesamiento de documentos y generación de embeddings.
- Las cachés de embeddings son archivos generados localmente y no forman parte del repositorio.
- Los resultados de recuperación pueden variar según los modelos y las versiones de las dependencias.
- Los documentos del corpus deben conservarse en la carpeta `documentos/` para reproducir el procesamiento completo.

## Autoría

Proyecto académico de procesamiento de lenguaje natural.
