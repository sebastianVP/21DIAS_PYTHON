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
from langchain_community.embeddings import HuggingFaceEmbeddings
#from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
#from langchain_qdrant import QdrantVectorStore
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
"""
Es una abstracción de alto nivel que combina:
La conexión a Qdrant.
El modelo de embeddings.
Los métodos para almacenar y buscar documentos similares.
"""
#vectorStore = QdrantVectorStore(
try:
    vectorStore = Qdrant(
        client          = client,
        collection_name = collection_name,
        embeddings      = embeddings,
        content_payload_key="texto",  # 👈 clave correcta en tu Qdrant por default es "page_content"
    )
    print(f"✅ VectorStore creado correctamente para la colección: {collection_name}")
except Exception as e:
    print(f"❌ Error al crear el VectorStore: {e}")


# Retriever,Es el componente que hace las búsquedas dentro del VectorStore.
"""
Es el componente que hace las búsquedas dentro del VectorStore.
search_type="similarity" indica que queremos buscar por similitud de coseno (los documentos con embeddings más cercanos al de la pregunta).
search_kwargs={"k": 3} significa: “devuélveme los 3 documentos más parecidos”.
"""
retriever = vectorStore.as_retriever(search_type="similarity",search_kwargs={"k":3})

## AQUI VIENE EL LLM
llm = OllamaLLM(model="llama3",temperatura=0)

# Prompt

prompt = ChatPromptTemplate.from_template(
"""
usa el siguiente contexto para responder la pregunta de manera concisa.
si no hay informacion suficiente, responde que no lo sabes.

contexto:
{context}                                          
                                          
pregunta:
{question}                                          
"""
)

# CADENA RAG
"""
💡 Aquí se construye la pipeline completa:
RunnableParallel(...) ejecuta dos cosas:
Pasa la pregunta al retriever para obtener el contexto.
Pasa la pregunta al modelo como {question}.
Luego todo se pasa al prompt, que forma el texto final con contexto + pregunta.
Finalmente, se envía al llm para que genere la respuesta final.

EJECUCION:
uvicorn api:app --reload --host 0.0.0.0 --port 8000

"""
rag_chain = (
RunnableParallel({"context":retriever,"question":RunnablePassthrough()})
| prompt
| llm
)

#-----------
#4️⃣ Endpoint de consulta
#------------
@app.post("/ask")
def ask_question(request:QueryRequest):
    try:
        respuesta = rag_chain.invoke(request.question)
        return {"question":request.question,"answer":respuesta}
    except Exception as e:
        return {"error":str(e)}
    