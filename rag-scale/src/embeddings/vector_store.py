
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from .embedder import load_embedder

def init_vector_db(chunks, collection_name="docs_100pdfs"):
    # 1️⃣ Conectar al Qdrant
    client = QdrantClient(url="http://localhost:6333")
    # 2️⃣ Cargar embeddings
    embeddings = load_embedder()

    # 2. Construir textos y metadatos
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]

    # 3 Crear vectorstore en Qdrant
    vector_db = QdrantVectorStore.from_texts(
        texts=texts,
        metadatas=metadatas,
        embedding=embeddings,
        url="http://localhost:6333",          # <--- ESTA ES LA CLAVE
        prefer_grpc=False,                    # gRPC opcional
        collection_name=collection_name,
        content_payload_key="text",
    )

    return vector_db

def init_vector_collection_ready_db(collection_name="docs_100pdfs"):
    # 1️⃣ Conectar al Qdrant
    client = QdrantClient(url="http://localhost:6333")
    # 2️⃣ Cargar embeddings
    embeddings = load_embedder()

    vector_db = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
        content_payload_key="texto"  # 👈 clave correcta en tu Qdrant por default es "page_content"
    )
    return vector_db
