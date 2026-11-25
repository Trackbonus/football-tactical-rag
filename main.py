"""
Football Tactical RAG
---------------------

Sistema de recuperación aumentada por generación (RAG) orientado
a responder preguntas sobre táctica de fútbol utilizando documentos
PDF como fuente de conocimiento.

Flujo general:
1. Carga y extracción de texto desde documentos PDF.
2. Fragmentación del contenido mediante estrategia fija o semántica.
3. Generación y almacenamiento de embeddings.
4. Recuperación de información mediante embeddings, TF-IDF o un
   enfoque híbrido que combina embeddings y BM25.
5. Reordenamiento de candidatos mediante un modelo CrossEncoder.
6. Expansión opcional de la recuperación dentro de los documentos
   identificados como relevantes.
7. Generación de respuestas fundamentadas en los fragmentos
   recuperados mediante un modelo de lenguaje local.

Ejecución:
    python main.py

Requisitos principales:
    - Ollama en ejecución.
    - Modelo de lenguaje: gemma3:4b.
    - Modelo de embeddings: embeddinggemma.
    - Documentos PDF dentro de la carpeta documentos.
"""

import logging
import json
import os
import re
import time
import uuid
import hashlib
from pathlib import Path

import ollama
import numpy as np
import pymupdf

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import CrossEncoder


# --------------------------------------------------
# 1. Configuración
# --------------------------------------------------

# Modelos locales utilizados para generar respuestas y embeddings.
MODEL = "gemma3:4b"
EMBEDDING_MODEL = "embeddinggemma"

# Rutas principales del proyecto.
PROJECT_FOLDER = Path(__file__).resolve().parent
DOCUMENTS_FOLDER = PROJECT_FOLDER / "documentos"

# Parámetros de fragmentación fija.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Estrategia de fragmentación seleccionable mediante una variable
# de entorno: "fixed" o "semantic".
CHUNKING_STRATEGY = os.getenv(
    "CHUNKING_STRATEGY", "semantic"
).strip().lower()

# Parámetros de fragmentación semántica.
SEMANTIC_MIN_CHARS = 400
SEMANTIC_MAX_CHARS = 1600
SEMANTIC_SIMILARITY_THRESHOLD = 0.68
SEMANTIC_EMBEDDING_BATCH_SIZE = 32

# Número de fragmentos finales que se utilizarán como contexto.
TOP_K = 4

# Método de recuperación: "embeddings", "tfidf" o "hybrid".
RETRIEVAL_METHOD = "hybrid"

# Indica si se incorporan fragmentos vecinos durante la recuperación.
INCLUDE_NEIGHBORS = False

# Parámetros de generación y almacenamiento de embeddings.
EMBEDDING_BATCH_SIZE = 8
CACHE_PATH = PROJECT_FOLDER / "embeddings_cache.npz"

# Caché utilizada durante la fragmentación semántica.
SEMANTIC_SENTENCE_CACHE_PATH = (
    PROJECT_FOLDER / "semantic_sentence_embeddings_cache.npz"
)

# Modelo CrossEncoder utilizado para reordenar los candidatos.
RERANKER_MODEL = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
RERANKER_BATCH_SIZE = 4


# Configuración del registro de eventos del programa.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


# --------------------------------------------------
# 2. Carga y extracción de documentos
# --------------------------------------------------

def load_documents():
    """
    Busca y devuelve los archivos PDF disponibles en la carpeta
    documentos.

    Los archivos se ordenan alfabéticamente para mantener un orden
    reproducible durante el procesamiento.
    """

    if not DOCUMENTS_FOLDER.exists():
        raise FileNotFoundError(
            f"No existe la carpeta: {DOCUMENTS_FOLDER}"
        )

    pdf_files = sorted(DOCUMENTS_FOLDER.glob("*.pdf"))

    if not pdf_files:
        raise ValueError("No se encontraron documentos PDF.")

    logging.info(f"Se encontraron {len(pdf_files)} documentos.")

    return pdf_files


def extract_text_from_pdf(pdf_path):
    """
    Extrae el texto de cada página de un documento PDF.

    Cada página se almacena como un registro independiente que
    conserva el nombre del documento de origen y su número de página.
    Las páginas sin texto se omiten.
    """

    pages = []

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text().strip()

            if text:
                pages.append({
                    "text": text,
                    "source": pdf_path.name,
                    "page": page_number
                })

    return pages


# --------------------------------------------------
# 3. Fragmentación del texto
# --------------------------------------------------

def chunk_text(pages):
    """
    Divide el texto de las páginas en fragmentos de tamaño fijo.

    Se utiliza un solapamiento entre fragmentos consecutivos para
    reducir la pérdida de contexto en los límites de cada fragmento.

    Cada fragmento conserva los metadatos del documento y la página
    de la que fue extraído.
    """

    chunks = []
    step = CHUNK_SIZE - CHUNK_OVERLAP

    for page in pages:
        text = page["text"]

        for start in range(0, len(text), step):
            chunk = text[start:start + CHUNK_SIZE]

            if chunk.strip():
                chunks.append({
                    "text": chunk,
                    "source": page["source"],
                    "page": page["page"]
                })

    return chunks


def _split_sentences(text):
    """
    Identifica los rangos de las oraciones presentes en un texto.

    Devuelve las posiciones inicial y final de cada oración sin
    modificar el contenido original.
    """

    return [
        (match.start(), match.end())
        for match in re.finditer(
            r"\S.*?(?:[.!?](?=\s|$)|$)",
            text,
            re.DOTALL
        )
    ]


def _split_oversized_text(text, max_chars):
    """
    Divide una oración que supera el tamaño máximo permitido.

    La división se intenta realizar en espacios para evitar cortar
    palabras. Si no existe un espacio adecuado, se utiliza el límite
    máximo de caracteres.
    """

    parts = []
    start = 0

    while len(text) - start > max_chars:
        end = text.rfind(" ", start, start + max_chars + 1)

        if end <= start:
            end = start + max_chars

        parts.append((start, end))
        start = end

    if start < len(text):
        parts.append((start, len(text)))

    return parts


def chunk_text_semantic(pages):
    """
    Agrupa oraciones en fragmentos mediante similitud semántica.

    Primero identifica las oraciones de cada página y genera sus
    embeddings. Después compara las oraciones consecutivas y utiliza
    su similitud para determinar los límites de los fragmentos.

    Se respetan tamaños mínimos y máximos para evitar fragmentos
    demasiado pequeños o demasiado extensos.

    Los embeddings de las oraciones se almacenan en una caché.
    Si el contenido del corpus y los parámetros no han cambiado,
    se reutilizan los embeddings existentes.
    """

    prepared_pages = []
    hasher = hashlib.sha256()

    # La huella identifica el corpus y los parámetros utilizados
    # para generar los embeddings de las oraciones.
    for value in (
        EMBEDDING_MODEL,
        str(SEMANTIC_MIN_CHARS),
        str(SEMANTIC_MAX_CHARS),
        str(SEMANTIC_SIMILARITY_THRESHOLD),
        str(SEMANTIC_EMBEDDING_BATCH_SIZE)
    ):
        hasher.update(value.encode("utf-8"))
        hasher.update(b"\0")

    # Separar cada página en unidades de texto.
    for page in pages:
        text = page["text"]
        sentences = _split_sentences(text)
        units = []

        for start, end in sentences:
            if end - start > SEMANTIC_MAX_CHARS:
                units.extend(
                    (start + a, start + b)
                    for a, b in _split_oversized_text(
                        text[start:end],
                        SEMANTIC_MAX_CHARS
                    )
                )
            else:
                units.append((start, end))

        unit_texts = [text[a:b] for a, b in units]
        prepared_pages.append((page, units, unit_texts))

        # Incorporar el contenido y sus metadatos a la huella.
        for sentence in unit_texts:
            hasher.update(page["source"].encode("utf-8"))
            hasher.update(str(page["page"]).encode("utf-8"))
            hasher.update(sentence.encode("utf-8"))
            hasher.update(b"\0")

    fingerprint = hasher.hexdigest()

    all_units = [
        sentence
        for _, _, unit_texts in prepared_pages
        for sentence in unit_texts
    ]

    all_vectors = None

    # Comprobar si existe una caché compatible con el corpus actual.
    if SEMANTIC_SENTENCE_CACHE_PATH.exists():
        try:
            with np.load(
                SEMANTIC_SENTENCE_CACHE_PATH,
                allow_pickle=False
            ) as cache:

                if (
                    str(cache["fingerprint"].item()) == fingerprint
                    and cache["embeddings"].shape[0] == len(all_units)
                ):
                    all_vectors = cache["embeddings"]
                    logging.info(
                        "Caché de embeddings de oraciones: reutilizada"
                    )

        except Exception as error:
            logging.warning(
                f"No se pudo leer la caché semántica de oraciones: {error}"
            )

    # Si no existe una caché válida, generar los embeddings por lotes.
    if all_vectors is None:
        generated = []

        for batch_start in range(
            0,
            len(all_units),
            SEMANTIC_EMBEDDING_BATCH_SIZE
        ):
            batch = all_units[
                batch_start:
                batch_start + SEMANTIC_EMBEDDING_BATCH_SIZE
            ]

            response = ollama.embed(
                model=EMBEDDING_MODEL,
                input=batch
            )

            generated.extend(response["embeddings"])

        all_vectors = np.asarray(generated, dtype=np.float32)

        # Guardar la caché mediante un archivo temporal para evitar
        # reemplazar directamente el archivo definitivo.
        temp_path = SEMANTIC_SENTENCE_CACHE_PATH.with_name(
            f"{SEMANTIC_SENTENCE_CACHE_PATH.stem}.tmp.npz"
        )

        with open(temp_path, "wb") as cache_file:
            np.savez_compressed(
                cache_file,
                embeddings=all_vectors,
                fingerprint=np.array(fingerprint)
            )

        temp_path.replace(SEMANTIC_SENTENCE_CACHE_PATH)

        logging.info("Caché de embeddings de oraciones: generada")

    # Agrupar las oraciones según su similitud semántica.
    chunks = []
    vector_offset = 0

    for page, units, unit_texts in prepared_pages:
        text = page["text"]

        vectors = all_vectors[
            vector_offset:vector_offset + len(units)
        ]

        vector_offset += len(units)

        if not units:
            continue

        vectors = np.asarray(vectors, dtype=np.float32)
        norms = np.linalg.norm(vectors, axis=1)

        boundaries = []

        # Una similitud inferior al umbral indica una posible
        # separación entre dos fragmentos.
        for i in range(len(units) - 1):
            denom = norms[i] * norms[i + 1]

            similarity = (
                float(
                    np.dot(vectors[i], vectors[i + 1]) / denom
                )
                if denom
                else 0.0
            )

            boundaries.append(
                similarity < SEMANTIC_SIMILARITY_THRESHOLD
            )

        group_start = 0

        for i in range(1, len(units)):
            start_char = units[group_start][0]
            previous_end = units[i - 1][1]
            next_end = units[i][1]

            current_size = previous_end - start_char
            proposed_size = next_end - start_char

            # Separar cuando cambia suficientemente el contenido
            # semántico o cuando se supera el tamaño máximo.
            should_split = (
                boundaries[i - 1]
                and current_size >= SEMANTIC_MIN_CHARS
            )

            should_split = (
                should_split
                or proposed_size > SEMANTIC_MAX_CHARS
            )

            if should_split:
                chunk = text[start_char:units[i][0]]

                if chunk.strip():
                    chunks.append({
                        "text": chunk,
                        "source": page["source"],
                        "page": page["page"]
                    })

                group_start = i

        # Incorporar el último grupo de la página.
        chunk = text[units[group_start][0]:]

        if chunk.strip():
            chunks.append({
                "text": chunk,
                "source": page["source"],
                "page": page["page"]
            })

    return chunks


def export_chunks(chunks, path):
    """
    Exporta los fragmentos a un archivo JSON.

    Se conservan el texto y los metadatos de cada fragmento para
    permitir su inspección y reutilización posterior.
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as output:
        json.dump(
            chunks,
            output,
            ensure_ascii=False,
            indent=2
        )


# --------------------------------------------------
# 4. Generación de embeddings
# --------------------------------------------------

def generate_embeddings(chunks, strategy="fixed"):
    """
    Genera embeddings para todos los fragmentos del corpus.

    El procesamiento se realiza por lotes de tamaño fijo. Después
    de cada lote, los embeddings se guardan en un checkpoint para
    permitir reanudar la generación si ocurre una interrupción.

    Antes de reutilizar una caché, se verifica que corresponda
    exactamente al corpus y a la estrategia de fragmentación actuales.
    """

    if EMBEDDING_BATCH_SIZE != 8:
        raise ValueError(
            "EMBEDDING_BATCH_SIZE debe mantenerse en 8."
        )

    # Crear una huella que identifica los fragmentos y el modelo.
    hasher = hashlib.sha256()
    hasher.update(strategy.encode("utf-8"))
    hasher.update(EMBEDDING_MODEL.encode("utf-8"))

    for chunk in chunks:
        hasher.update(chunk["source"].encode("utf-8"))
        hasher.update(str(chunk["page"]).encode("utf-8"))
        hasher.update(chunk["text"].encode("utf-8"))

    fingerprint = hasher.hexdigest()

    cache_path = CACHE_PATH.with_name(
        f"embeddings_cache_{strategy}.npz"
    )

    legacy_temp_path = cache_path.with_name(
        f"{cache_path.stem}.tmp.npz"
    )

    # Buscar la caché definitiva y los checkpoints disponibles.
    checkpoint_paths = []

    if cache_path.exists():
        checkpoint_paths.append(cache_path)

    if legacy_temp_path.exists():
        checkpoint_paths.append(legacy_temp_path)

    checkpoint_paths.extend(
        sorted(
            cache_path.parent.glob(
                f"{cache_path.stem}.checkpoint.*.tmp.npz"
            )
        )
    )

    valid_checkpoints = []

    # Comprobar la integridad y compatibilidad de cada checkpoint.
    for checkpoint_path in checkpoint_paths:
        try:
            with np.load(
                checkpoint_path,
                allow_pickle=False
            ) as cache:

                candidate_fingerprint = str(
                    cache["fingerprint"].item()
                )

                candidate_embeddings = np.asarray(
                    cache["embeddings"],
                    dtype=np.float32
                )

                candidate_completed = int(
                    cache["completed"].item()
                )

        except Exception as error:
            logging.warning(
                f"Se conserva el checkpoint no legible "
                f"{checkpoint_path.name}: {error}"
            )
            continue

        consistent = (
            candidate_fingerprint == fingerprint
            and candidate_embeddings.ndim == 2
            and 0 <= candidate_completed <= len(chunks)
            and candidate_embeddings.shape[0] == candidate_completed
            and candidate_embeddings.shape[1] > 0
            and np.isfinite(candidate_embeddings).all()
        )

        if consistent:
            valid_checkpoints.append((
                candidate_completed,
                checkpoint_path,
                candidate_embeddings
            ))
        else:
            logging.warning(
                "Se conserva sin usar el checkpoint incompatible "
                f"o inconsistente: {checkpoint_path.name}"
            )

    # Si existen varios checkpoints, verificar que los más avanzados
    # extiendan exactamente los resultados de los anteriores.
    valid_checkpoints.sort(key=lambda item: item[0])

    accepted = None

    for candidate in valid_checkpoints:
        if accepted is None:
            accepted = candidate
            continue

        previous_count, previous_path, previous_embeddings = accepted
        count, path, embeddings_candidate = candidate

        if count < previous_count:
            continue

        if not np.array_equal(
            previous_embeddings,
            embeddings_candidate[:previous_count]
        ):
            raise RuntimeError(
                f"El checkpoint {path.name} no extiende exactamente "
                f"{previous_path.name}; se conservan ambos sin modificar."
            )

        accepted = candidate

    embeddings = np.empty((0, 0), dtype=np.float32)
    completed = 0

    if accepted is not None:
        completed, checkpoint_path, embeddings = accepted

        logging.info(
            f"Checkpoint de embeddings recuperado desde "
            f"{checkpoint_path.name}: {completed}/{len(chunks)}"
        )

    # Evitar sobrescribir una caché definitiva que no sea compatible.
    if (
        cache_path.exists()
        and not any(
            path == cache_path
            for _, path, _ in valid_checkpoints
        )
    ):
        raise RuntimeError(
            f"La caché oficial {cache_path.name} no es válida "
            "para esta huella; se conserva sin modificar y "
            "no se sobrescribirá."
        )

    # Generar los embeddings pendientes y guardar cada checkpoint.
    for start in range(
        completed,
        len(chunks),
        EMBEDDING_BATCH_SIZE
    ):
        end = min(
            start + EMBEDDING_BATCH_SIZE,
            len(chunks)
        )

        batch_texts = [
            chunk["text"]
            for chunk in chunks[start:end]
        ]

        response = ollama.embed(
            model=EMBEDDING_MODEL,
            input=batch_texts
        )

        batch_embeddings = np.asarray(
            response["embeddings"],
            dtype=np.float32
        )

        if (
            batch_embeddings.ndim != 2
            or batch_embeddings.shape[0] != end - start
        ):
            raise RuntimeError(
                f"Ollama devolvió "
                f"{batch_embeddings.shape[0] if batch_embeddings.ndim else 0} "
                f"embeddings para el lote de {end - start} chunks."
            )

        if (
            embeddings.size
            and batch_embeddings.shape[1] != embeddings.shape[1]
        ):
            raise RuntimeError(
                "La dimensión de embeddings cambió durante la generación."
            )

        embeddings = (
            batch_embeddings
            if not embeddings.size
            else np.concatenate(
                (embeddings, batch_embeddings),
                axis=0
            )
        )

        completed = end

        # Cada intento utiliza un nombre exclusivo. Si falla la
        # publicación, el checkpoint temporal queda disponible
        # para intentar recuperar el progreso posteriormente.
        temp_path = cache_path.with_name(
            f"{cache_path.stem}.checkpoint."
            f"{uuid.uuid4().hex}.tmp.npz"
        )

        with open(temp_path, "xb") as file:
            np.savez_compressed(
                file,
                embeddings=embeddings,
                fingerprint=np.array(fingerprint),
                completed=np.array(completed)
            )

            file.flush()
            os.fsync(file.fileno())

        # Reintentar la publicación ante bloqueos temporales
        # del archivo, especialmente en Windows.
        last_error = None

        for attempt, delay in enumerate(
            (0, 0.25, 0.5, 1.0, 2.0),
            start=1
        ):
            if delay:
                time.sleep(delay)

            try:
                os.replace(temp_path, cache_path)
                last_error = None
                break

            except PermissionError as error:
                last_error = error

            except OSError as error:
                # Windows: 5 = acceso denegado;
                # 32/33 = archivo en uso.
                if getattr(error, "winerror", None) not in {5, 32, 33}:
                    raise

                last_error = error

        if last_error is not None:
            raise RuntimeError(
                f"No se pudo publicar el checkpoint de "
                f"{completed} embeddings después de 5 intentos. "
                f"El checkpoint recuperable se conserva en "
                f"{temp_path.name}; la caché anterior "
                f"{cache_path.name} no se modificó."
            ) from last_error

        logging.info(
            f"Embeddings guardados: {completed}/{len(chunks)}"
        )

    return embeddings


# --------------------------------------------------
# 5. Recuperación de información
# --------------------------------------------------

def retrieve_relevant_chunks(
    question,
    chunks,
    embeddings,
    top_k=TOP_K
):
    """
    Recupera fragmentos mediante similitud semántica.

    Genera el embedding de la pregunta, calcula su similitud coseno
    con los embeddings del corpus y devuelve los fragmentos mejor
    posicionados.

    Si INCLUDE_NEIGHBORS está activado, también incorpora fragmentos
    adyacentes de la misma página y documento.
    """

    question_embedding = ollama.embed(
        model=EMBEDDING_MODEL,
        input=question
    )["embeddings"][0]

    similarities = cosine_similarity(
        [question_embedding],
        embeddings
    )[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    included_indices = set()

    for index in top_indices:

        if INCLUDE_NEIGHBORS:
            neighbor_indices = range(
                max(0, index - 1),
                min(len(chunks), index + 2)
            )
        else:
            neighbor_indices = [index]

        for neighbor_index in neighbor_indices:
            if neighbor_index in included_indices:
                continue

            # Evitar incorporar fragmentos de otra página
            # o de otro documento.
            if (
                chunks[neighbor_index]["source"]
                != chunks[index]["source"]
                or chunks[neighbor_index]["page"]
                != chunks[index]["page"]
            ):
                continue

            included_indices.add(neighbor_index)

            results.append({
                "text": chunks[neighbor_index]["text"],
                "source": chunks[neighbor_index]["source"],
                "page": chunks[neighbor_index]["page"],
                "similarity": similarities[neighbor_index],
                "index": neighbor_index
            })

    return results


def retrieve_relevant_chunks_tfidf(
    question,
    chunks,
    vectorizer,
    tfidf_matrix,
    top_k=TOP_K
):
    """
    Recupera fragmentos mediante similitud TF-IDF.

    Transforma la pregunta utilizando el vocabulario aprendido
    durante la vectorización del corpus y calcula la similitud coseno
    entre la pregunta y cada fragmento.
    """

    # Transformar la pregunta con el mismo vocabulario del corpus.
    question_vector = vectorizer.transform([question])

    # Calcular la similitud entre la pregunta y los fragmentos.
    similarities = cosine_similarity(
        question_vector,
        tfidf_matrix
    )[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    included_indices = set()

    for index in top_indices:

        if INCLUDE_NEIGHBORS:
            neighbor_indices = range(
                max(0, index - 1),
                min(len(chunks), index + 2)
            )
        else:
            neighbor_indices = [index]

        for neighbor_index in neighbor_indices:
            if neighbor_index in included_indices:
                continue

            if (
                chunks[neighbor_index]["source"]
                != chunks[index]["source"]
                or chunks[neighbor_index]["page"]
                != chunks[index]["page"]
            ):
                continue

            included_indices.add(neighbor_index)

            results.append({
                "text": chunks[neighbor_index]["text"],
                "source": chunks[neighbor_index]["source"],
                "page": chunks[neighbor_index]["page"],
                "similarity": similarities[neighbor_index],
                "index": neighbor_index
            })

    return results


def retrieve_relevant_chunks_hybrid(
    question,
    chunks,
    embeddings,
    reranker
):
    """
    Realiza recuperación híbrida mediante embeddings y BM25.

    Primero obtiene candidatos mediante similitud semántica.
    Después calcula puntuaciones BM25 para identificar coincidencias
    léxicas entre la pregunta y los fragmentos.

    Ambas listas se combinan sin duplicados y los candidatos
    resultantes se reordenan mediante un CrossEncoder.

    Finalmente, devuelve los TOP_K fragmentos con mayor puntuación
    de re-ranking.
    """

    # 1. Recuperar los 30 mejores candidatos mediante embeddings.
    embedding_results = retrieve_relevant_chunks(
        question,
        chunks,
        embeddings,
        top_k=30
    )

    # 2. Calcular puntuaciones BM25.
    # La tokenización utiliza palabras en minúsculas y conserva
    # caracteres Unicode, incluidos los acentos.
    def tokenize(text):
        return re.findall(
            r"\w+",
            text.casefold(),
            flags=re.UNICODE
        )

    documents = [
        tokenize(chunk["text"])
        for chunk in chunks
    ]

    query_tokens = tokenize(question)

    n_documents = len(documents)

    document_lengths = np.array(
        [len(doc) for doc in documents],
        dtype=np.float32
    )

    average_length = float(document_lengths.mean())

    # Frecuencia de documentos: número de fragmentos que contienen
    # cada término, independientemente de cuántas veces aparezca.
    document_frequencies = {}

    for document in documents:
        for term in set(document):
            document_frequencies[term] = (
                document_frequencies.get(term, 0) + 1
            )

    # Parámetros habituales de BM25.
    k1 = 1.5
    b = 0.75

    bm25_scores = np.zeros(
        n_documents,
        dtype=np.float32
    )

    for term in query_tokens:
        df = document_frequencies.get(term, 0)

        if df == 0:
            continue

        idf = np.log(
            1 + (n_documents - df + 0.5) / (df + 0.5)
        )

        for index, document in enumerate(documents):
            term_frequency = document.count(term)

            if term_frequency == 0:
                continue

            denominator = (
                term_frequency
                + k1 * (
                    1 - b
                    + b * document_lengths[index] / average_length
                )
            )

            bm25_scores[index] += (
                idf
                * term_frequency
                * (k1 + 1)
                / denominator
            )

    # Seleccionar los 30 candidatos mejor puntuados por BM25.
    bm25_indices = np.argsort(bm25_scores)[::-1][:30]

    bm25_results = [
        {
            "index": int(index),
            "text": chunks[index]["text"],
            "source": chunks[index]["source"],
            "page": chunks[index]["page"],
            "similarity": float(bm25_scores[index])
        }
        for index in bm25_indices
    ]

    # 3. Unir los candidatos de ambos métodos sin duplicados.
    candidate_indices = list(dict.fromkeys(
        [result["index"] for result in embedding_results]
        + [result["index"] for result in bm25_results]
    ))

    # 4. Evaluar la relevancia de cada candidato mediante CrossEncoder.
    pairs = [
        (question, chunks[index]["text"])
        for index in candidate_indices
    ]

    rerank_scores = reranker.predict(
        pairs,
        batch_size=RERANKER_BATCH_SIZE
    )

    # 5. Seleccionar los cuatro candidatos con mayor puntuación.
    selected_positions = np.argsort(rerank_scores)[::-1][:TOP_K]

    results = []

    for position in selected_positions:
        index = candidate_indices[position]

        results.append({
            "index": index,
            "text": chunks[index]["text"],
            "source": chunks[index]["source"],
            "page": chunks[index]["page"],
            "rerank_score": float(rerank_scores[position])
        })

    return results


# --------------------------------------------------
# 6. Expansión de la recuperación por documento
# --------------------------------------------------

def expand_retrieval_by_document(
    query,
    retrieved_chunks,
    all_chunks,
    reranker,
    top_k=TOP_K
):
    """
    Amplía la recuperación utilizando los documentos identificados
    como más relevantes en la primera etapa.

    Selecciona los dos primeros documentos de la recuperación inicial,
    incorpora sus fragmentos al conjunto de candidatos y los vuelve
    a evaluar mediante el CrossEncoder.

    Devuelve los fragmentos mejor posicionados después de esta
    segunda etapa de re-ranking.
    """

    if not retrieved_chunks:
        return []

    # Identificar los dos documentos mejor posicionados.
    selected_sources = []

    for chunk in retrieved_chunks[:2]:
        source = chunk["source"]

        if source not in selected_sources:
            selected_sources.append(source)

    # Conservar los fragmentos recuperados inicialmente.
    candidates = {}

    for chunk in retrieved_chunks:
        candidates[chunk["index"]] = chunk

    # Incorporar los fragmentos restantes de los documentos elegidos.
    for index, chunk in enumerate(all_chunks):
        if chunk["source"] in selected_sources:
            candidates[index] = {
                **chunk,
                "index": index
            }

    candidate_list = list(candidates.values())

    if not candidate_list:
        return []

    # Reordenar todos los candidatos con el CrossEncoder.
    pairs = [
        (query, chunk["text"])
        for chunk in candidate_list
    ]

    scores = reranker.predict(
        pairs,
        batch_size=RERANKER_BATCH_SIZE,
        show_progress_bar=False
    )

    for chunk, score in zip(candidate_list, scores):
        chunk["rerank_score"] = float(score)

    candidate_list.sort(
        key=lambda chunk: chunk["rerank_score"],
        reverse=True
    )

    return candidate_list[:top_k]


# --------------------------------------------------
# 7. Generación de respuestas
# --------------------------------------------------

def generate_answer(question, relevant_chunks):
    """
    Genera una respuesta en español a partir de los fragmentos
    recuperados.

    Los fragmentos se entregan al modelo de lenguaje como contexto.
    El prompt restringe la respuesta a la información del corpus,
    solicita referencias a documentos y páginas y pide reconocer
    explícitamente las limitaciones de la evidencia disponible.
    """

    if not relevant_chunks:
        return (
            "No hay evidencia suficiente en los fragmentos "
            "recuperados para responder la pregunta."
        )

    # Preparar el contexto y conservar las referencias de procedencia.
    context_data = [
        {
            "text": chunk["text"],
            "source": chunk["source"],
            "page": chunk["page"]
        }
        for chunk in relevant_chunks
    ]

    context = json.dumps(
        context_data,
        ensure_ascii=False
    )

    # Instrucciones para generar respuestas fundamentadas en el corpus.
    prompt = f"""Responde directamente a la pregunta en español con una explicación natural, coherente y útil.

Utiliza exclusivamente la información contenida en los fragmentos proporcionados. No inventes datos ni atribuyas a los documentos afirmaciones que no aparecen en ellos.

Los fragmentos son textos originales recuperados directamente del corpus. Puedes resumirlos, traducirlos, relacionarlos y parafrasearlos. No necesitas reproducir citas textuales.

Distingue claramente entre:
- Información explícita en los documentos.
- Interpretaciones o inferencias propias, identificándolas como tales.

Nunca atribuyas a una fuente una explicación, mecanismo causal, estadística o conclusión que no esté contenida en los fragmentos.

Cada afirmación basada en el corpus debe incluir la referencia al documento y página correspondiente, con el formato (documento, p. X).

Si la evidencia es limitada, responde lo que puedas fundamentar y señala brevemente sus límites. Si los fragmentos no permiten responder, indícalo sin inventar información.

Prioriza una respuesta directa, clara y proporcionada a la pregunta.

PREGUNTA:
{question}

FRAGMENTOS RECUPERADOS:
{context}"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# --------------------------------------------------
# 8. Programa principal
# --------------------------------------------------

def main():
    """
    Ejecuta el flujo completo del sistema Football Tactical RAG.

    Prepara el corpus, genera o reutiliza los embeddings, carga
    el modelo de re-ranking y habilita la interacción con el usuario.

    El programa permanece activo hasta que se introduce el comando
    'salir'.
    """

    print("=== FOOTBALL TACTICAL RAG ===\n")

    try:
        # 1. Cargar los documentos PDF.
        pdf_files = load_documents()

        # 2. Extraer el texto y sus metadatos de procedencia.
        pages = []

        for pdf_path in pdf_files:
            pages.extend(
                extract_text_from_pdf(pdf_path)
            )

        if not pages:
            raise ValueError(
                "No se pudo extraer texto de los PDF."
            )

        logging.info(
            f"Se extrajo texto de {len(pages)} páginas."
        )

        # 3. Validar y aplicar la estrategia de fragmentación.
        if CHUNKING_STRATEGY not in {"fixed", "semantic"}:
            raise ValueError(
                "CHUNKING_STRATEGY debe ser 'fixed' o 'semantic'."
            )

        logging.info(
            f"Estrategia seleccionada: {CHUNKING_STRATEGY}"
        )

        if CHUNKING_STRATEGY == "semantic":
            semantic_chunks_path = (
                PROJECT_FOLDER
                / "resultados"
                / "chunks_semanticos.json"
            )

            # Reutilizar los fragmentos semánticos si ya existen.
            if semantic_chunks_path.exists():
                with semantic_chunks_path.open(
                    "r",
                    encoding="utf-8"
                ) as source:
                    chunks = json.load(source)

                logging.info(
                    f"Chunks semánticos cargados: {len(chunks)}"
                )

                logging.info(
                    "Caché de embeddings de oraciones: "
                    "no requerida (chunks semánticos reutilizados)"
                )

            else:
                chunks = chunk_text_semantic(pages)

                export_chunks(
                    chunks,
                    semantic_chunks_path
                )

                logging.info(
                    f"Chunks semánticos generados: {len(chunks)}"
                )

        else:
            chunks = chunk_text(pages)

            export_chunks(
                chunks,
                PROJECT_FOLDER / "resultados" / "chunks_fijos.json"
            )

            logging.info(
                f"Chunks fijos generados: {len(chunks)}"
            )

        if not chunks:
            raise ValueError("No se generaron fragmentos.")

        logging.info(
            f"Se generaron {len(chunks)} chunks."
        )

        # 4. Preparar la representación TF-IDF del corpus.
        # Se utiliza cuando el método seleccionado es "tfidf".
        vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2)
        )

        tfidf_matrix = vectorizer.fit_transform(
            [chunk["text"] for chunk in chunks]
        )

        # 5. Generar o recuperar los embeddings del corpus.
        logging.info("Generando embeddings...")

        embeddings = generate_embeddings(
            chunks,
            strategy=CHUNKING_STRATEGY
        )

        logging.info("Sistema preparado.\n")

        # 6. Cargar el modelo CrossEncoder para el re-ranking.
        logging.info("Cargando modelo de re-ranking...")

        reranker = CrossEncoder(
            RERANKER_MODEL,
            device="cpu"
        )

        logging.info("Re-ranking preparado.\n")

        # 7. Iniciar el ciclo de preguntas y respuestas.
        while True:

            question = input(
                "\nPregunta (o 'salir'): "
            ).strip()

            if question.lower() == "salir":
                print("Finalizando sistema.")
                break

            if not question:
                continue

            # 8. Recuperar los fragmentos según el método seleccionado.
            if RETRIEVAL_METHOD == "embeddings":
                relevant_chunks = retrieve_relevant_chunks(
                    question,
                    chunks,
                    embeddings
                )

            elif RETRIEVAL_METHOD == "tfidf":
                relevant_chunks = retrieve_relevant_chunks_tfidf(
                    question,
                    chunks,
                    vectorizer,
                    tfidf_matrix
                )

            elif RETRIEVAL_METHOD == "hybrid":
                relevant_chunks = retrieve_relevant_chunks_hybrid(
                    question,
                    chunks,
                    embeddings,
                    reranker
                )

                # Ampliar la recuperación utilizando los documentos
                # más relevantes de la primera etapa.
                relevant_chunks = expand_retrieval_by_document(
                    question,
                    relevant_chunks,
                    chunks,
                    reranker,
                    TOP_K
                )

            else:
                raise ValueError(
                    "Método de recuperación desconocido."
                )

            # 9. Generar la respuesta utilizando los fragmentos
            # originales recuperados como evidencia.
            print(
                f"\nFragmentos utilizados como evidencia: "
                f"{len(relevant_chunks)}"
            )

            answer = generate_answer(
                question,
                relevant_chunks
            )

            print("\nRespuesta:")
            print(answer)

            # 10. Mostrar la procedencia de los fragmentos utilizados.
            print("\nFuentes recuperadas:")

            for chunk in relevant_chunks:
                score = chunk.get(
                    "rerank_score",
                    chunk.get("similarity")
                )

                score_text = (
                    f"{score:.4f}"
                    if score is not None
                    else "no disponible"
                )

                print(
                    f"chunk-{chunk['index'] + 1:05d} | "
                    f"{chunk['source']} | "
                    f"página {chunk['page']} | "
                    f"score: {score_text}"
                )

    except Exception as error:
        logging.error(
            f"Error en el sistema: {error}"
        )


if __name__ == "__main__":
    main()