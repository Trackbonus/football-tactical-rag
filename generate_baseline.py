
from pathlib import Path
import ollama

# Configuración
MODEL = "gemma3:4b"

PROMPT = """
Actúa como un desarrollador Python especializado en sistemas
RAG (Retrieval-Augmented Generation).

Implementa una primera versión funcional de un Mini-RAG llamado
Football Tactical RAG.

OBJETIVO:
Responder preguntas sobre táctica de fútbol utilizando
documentos PDF locales.

ENTORNO:
- Windows y Python.
- Ollama ejecutándose localmente.
- Modelo generativo: gemma3:4b.
- Modelo de embeddings: embeddinggemma.
- Librerías: ollama, pymupdf, numpy, pandas y scikit-learn.

ESTRUCTURA:
Los documentos PDF están en la carpeta "documentos/",
ubicada junto a main.py.

REQUISITOS:

1. Cargar automáticamente todos los PDF de "documentos/".
2. Extraer el texto de todas las páginas con PyMuPDF.
3. Dividir el texto en chunks de aproximadamente 1000 caracteres,
   con un overlap de 200 caracteres.
4. Conservar el nombre del documento y número de página
   de cada chunk.
5. Generar embeddings con el modelo local embeddinggemma
   mediante Ollama.
6. Implementar recuperación semántica mediante similitud coseno.
7. Recuperar los cuatro chunks más relevantes para cada pregunta.
8. Construir un prompt con el contexto recuperado y la pregunta.
9. Generar respuestas con gemma3:4b mediante Ollama.
10. Mostrar las fuentes utilizadas, incluyendo documento y página.
11. Manejar errores como ausencia de documentos o texto vacío.
12. Permitir realizar múltiples preguntas desde la terminal
    hasta que el usuario decida salir.

RESTRICCIONES:
- No utilizar APIs externas ni servicios en la nube.
- No entrenar ni ajustar modelos.
- No utilizar bases de datos externas.
- Mantener el código sencillo, modular y fácil de explicar.
- Utilizar la API actual de la librería Python ollama.
- El programa debe poder ejecutarse con: python main.py

ENTREGA:
Primero explica brevemente la arquitectura.
Después entrega el código completo de main.py en un único
bloque Python.
No utilices pseudocódigo ni omitas funciones.
Incluye comentarios breves para explicar las secciones principales.
"""

# Generar respuesta utilizando el modelo local
print(f"Generando baseline con {MODEL}...")
print("Esto puede tardar unos minutos.\n")

response = ollama.chat(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": PROMPT
        }
    ]
)

raw_response = response["message"]["content"]

# Guardar la respuesta original sin modificarla
project_folder = Path(__file__).resolve().parent
baseline_folder = project_folder / "baseline"
baseline_folder.mkdir(exist_ok=True)

output_file = baseline_folder / "raw_response.md"
output_file.write_text(raw_response, encoding="utf-8")

print("Baseline generado correctamente.")
print(f"Respuesta guardada en: {output_file}")
print(f"Caracteres generados: {len(raw_response)}")
