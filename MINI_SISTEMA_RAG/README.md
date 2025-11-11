# ** 🧭QDRANT–LANGCHAIN BOOTCAMP**

## **Objetivo**: 

Construir un mini sistema RAG (Retrieval Augmented Generation) desde cero, entendiendo cada capa:
embeddings → indexación HNSW → almacenamiento vectorial → consulta semántica → respuesta con LLM.

NOTA: 🔹 HNSW (Hierarchical Navigable Small World)

**Comprender el flujo general y tener todo el entorno listo (local o nube).**

1.1 Concepto mental del pipeline RAG
Texto → Embedding → Base Vectorial (Qdrant/HNSW) → LangChain → LLM → Respuesta contextual

🧩 **Explicación rápida:**

- Cada documento se transforma en un vector numérico (embedding).
- Qdrant guarda esos vectores y usa HNSW para encontrar los más parecidos.
- LangChain coordina la búsqueda y genera la respuesta final con un LLM (OpenAI o local).

1.2 Instalación rápida (en tu entorno con Python)

Abre tu terminal y ejecuta:

pip install qdrant-client langchain sentence-transformers openai
pip install fastapi uvicorn # opcional si luego deseas servirlo vía API

Si usarás Qdrant local:

docker run -p 6333:6333 qdrant/qdrant


Verifica que está activo en:
👉 http://localhost:6333/dashboard

Si prefieres la nube:

Crea una cuenta en https://cloud.qdrant.io

Crea un cluster gratuito.

Obtén tu API Key y URL endpoint.