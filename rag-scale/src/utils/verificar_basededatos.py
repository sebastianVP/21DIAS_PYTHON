from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue


client = QdrantClient(url="http://localhost:6333")
collection_name = "docs_100pdfs"

# Mostrar algunos puntos almacenados
response = client.scroll(collection_name=collection_name, limit=3)

print("\n📦 Puntos en la colección:")
for point in response[0]:
    print(point.payload)
