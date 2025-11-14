# create_vector_db.py

from src.ingest.pipeline_ingest import ingest_all_pdfs
from src.embeddings.vector_store import init_vector_db

# 1. Procesar los 100 PDFs
chunks = ingest_all_pdfs()

# 2. Crear la colección en Qdrant con los chunks
db = init_vector_db(chunks, collection_name="docs_100pdfs")

print("Colección creada y lista.")
