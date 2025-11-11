from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
collection_name = "docs_vectorialesv2"

# Mostrar algunos puntos almacenados
response = client.scroll(collection_name=collection_name, limit=3)

print("\n📦 Puntos en la colección:")
for point in response[0]:
    print(point.payload)