"""
Vamos a armar un Servicio RAG Completo usando FastAPI +Uvicorn que exponga un 
endpoint para recibir preguntar y devolver respuestas generadas por el pipeline RAG.
Este ejemplo va a estar basado en :
- Qdrant: Base de datos vectorial
- Langchain: Framework de orquestacion de LLM,es una biblioteca que sirve como "pegamento" entre componentes de IA generativa,
 como modelos de lenguaje, bases de datos vectoriales y herramientas externas.
- OllamaLM: Servicio local de modelo de lenguaje:
    - llama3
    - mistral
    - phi3
    - gemma
    - codellama
    
flowchart TD
A[Usuario pregunta] --> B[LangChain]
B --> C[Conversión a embeddings]
C --> D[Qdrant Vector DB]
D -->|devuelve textos relevantes| E[LangChain]
E --> F[Ollama LLM]
F --> G[Respuesta contextualizada al usuario]

MINI_SISTEMA_RAG/
│
├─ rag_qdrant_langchain.py  # Pipeline RAG (creación de embeddings y vectorstore)
├─ api.py                   # Servicio FastAPI
├─ requirements.txt
└─ .gitignore               # Incluye .env
"""

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qrant import QdrantVectorStore
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from qdrant_client import QdrantClient

#-------
# 1️⃣ Configuracion de FastAPI
#-------

app = FastAPI(title="RAG-Qdrant- Ollama API")

#------
# 2️⃣ Modelo de request
#------
class QueryRequest(BaseModel):
    question: str

#--------
# 3️⃣ Inicializar pipeline RAG
#........
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Conexion Qdrant
client = QdrantClient(url="http://localhost:6333")
collection_name="docs_vectorialesv2"

# VectorStore
vectorStore = QdrantVectorStore(
    client          = client,
    collection_name = collection_name,
    embeddings      = embeddings
)

# Retriever,Es el componente que hace las búsquedas dentro del VectorStore.
