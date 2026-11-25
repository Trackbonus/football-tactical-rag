import os
import logging
import pymupdf
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from ollama import ollama

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Archivo de configuración de Ollama (puede ser necesario ajustarlo)
OLLAMA_MODEL = "gemma3:4b"
OLLAMA_EMBEDDING = "embeddinggemma"

# Carpeta que contiene los documentos PDF
DOCUMENTS_FOLDER = "documentos/"

def load_documents():
    """
    Carga todos los archivos PDF de la carpeta 'documentos/'.
    """
    if not os.path.exists(DOCUMENTS_FOLDER):
        logging.error(f"La carpeta '{DOCUMENTS_FOLDER}' no existe.")
        return []

    pdf_files = [f for f in os.listdir(DOCUMENTS_FOLDER) if f.endswith(".pdf")]
    logging.info(f"Se encontraron {len(pdf_files)} documentos PDF.")
    return pdf_files

def extract_text_from_pdf(pdf_file):
    """
    Extrae el texto de cada página de un archivo PDF usando PyMuPDF.
    """
    try:
        doc = pymupdf.open(os.path.join(DOCUMENTS_FOLDER, pdf_file))
        text = ""
        for page in doc.pages:
            text += page.extract_text()
        doc.close()
        return text
    except Exception as e:
        logging.error(f"Error al extraer texto de '{pdf_file}': {e}")
        return ""

def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Divide el texto en chunks con un overlap especificado.
    """
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

def generate_embeddings(chunks):
    """
    Genera embeddings para cada chunk usando el modelo embeddinggemma de Ollama.
    """
    try:
        embeddings = []
        for chunk in chunks:
            embedding = ollama.run(f"generate_embedding '{chunk}'", model=OLLAMA_EMBEDDING)
            embeddings.append(np.fromstring(embedding, sep=",").astype(np.float32)) # Parse embedding response as float array
        return np.array(embeddings)
    except Exception as e:
        logging.error(f"Error al generar embeddings: {e}")
        return None

def retrieve_relevant_chunks(question, embeddings, chunks):
    """
    Realiza recuperación semántica mediante similitud coseno.
    """
    question_embedding = np.fromstring(ollama.run(f"generate_embedding '{question}'", model=OLLAMA_EMBEDDING), sep=",").astype(np.float32)
    similarities = cosine_similarity([question_embedding], embeddings)[0]
    
    ranked_chunks = np.argsort(similarities)[::-1]  # Ordena por similitud
    return ranked_chunks

def build_prompt(question, context):
    """
    Construye el prompt para el modelo generativo.
    """
    prompt = f"Contexto:\n{context}\n\nPregunta: {question}\n\nRespuesta:"
    return prompt

def generate_answer(prompt):
    """
    Genera una respuesta con el modelo generativo gemma3:4b de Ollama.
    """
    try:
        response = ollama.run(prompt, model=OLLAMA_MODEL)
        return response
    except Exception as e:
        logging.error(f"Error al generar la respuesta: {e}")
        return ""

def main():
    """
    Función principal del programa.
    """
    # 1. Cargar documentos
    documents = load_documents()
    if not documents:
        print("No se encontraron documentos PDF.  Saliendo.")
        return

    # 2. Extraer texto de los documentos
    all_text = []
    for doc in documents:
        text = extract_text_from_pdf(doc)
        if text:
            all_text.append(text)

    # 3. Dividir el texto en chunks
    all_chunks = []
    for text in all_text:
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    # 4. Generar embeddings
    if all_chunks:
        embeddings = generate_embeddings(all_chunks)
        if embeddings is None:
            print("No se pudieron generar embeddings. Saliendo.")
            return
    else:
        print("No hay chunks disponibles para generar embeddings. Saliendo.")
        return

    # Bucle principal para interactuar con el usuario
    while True:
        question = input("Pregunta (o 'salir' para terminar): ")
        if question.lower() == "salir":
            break

        # 5. Recuperar chunks relevantes
        ranked_chunks = retrieve_relevant_chunks(question, embeddings, all_chunks)

        # 6. Construir prompt
        context = "\n".join([all_chunks[i] for i in ranked_chunks[:4]]) # Selecciona los 4 chunks más relevantes
        prompt = build_prompt(question, context)

        # 7. Generar respuesta
        answer = generate_answer(prompt)

        # 8. Mostrar resultados
        print(f"Respuesta: {answer}")
        print(f"Fuentes: {ranked_chunks}")

if __name__ == "__main__":
    main()