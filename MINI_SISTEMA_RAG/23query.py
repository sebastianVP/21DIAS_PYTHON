"""
Para borrar.
curl -X DELETE "http://localhost:6333/collections/docs_vectoriales"

"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams,PointStruct,HnswConfigDiff
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = QdrantClient(url="http://localhost:6333")  # o tu endpoint cloud

query = "¿Qué sistema se usa para analizar datos atmosféricos?"
query_vector = model.encode(query)

results = client.search(
    collection_name="docs_vectorialesv2",
    query_vector=query_vector,
    limit=3
)

for r in results:
    print(r.payload["texto"], "→", r.score)