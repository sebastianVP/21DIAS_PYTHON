# 🧭 Qdrant–LangChain – Mini Sistema RAG

## Objetivo
Construir un **mini sistema RAG (Retrieval Augmented Generation)** desde cero, entendiendo cada capa:

- Embeddings → Indexación HNSW → Almacenamiento vectorial → Consulta semántica → Respuesta con LLM.

> 🔹 HNSW: Hierarchical Navigable Small World.  
> Permite búsquedas vectoriales rápidas y precisas en grandes colecciones.

---

## Concepto del Pipeline RAG

```
Texto → Embedding → Base Vectorial (Qdrant/HNSW) → LangChain → LLM → Respuesta contextual
```

- Cada documento se transforma en un **vector numérico** (embedding).  
- **Qdrant** guarda esos vectores y usa HNSW para encontrar los más similares.  
- **LangChain** coordina la recuperación y genera la respuesta final usando un **LLM** (OpenAI o local, en este caso Ollama).  

---

## Instalación rápida

### 1️⃣ Entorno Python
Se recomienda crear un entorno limpio con Anaconda o venv:

```bash
conda create -n rag python=3.11 -y
conda activate rag
```

### 2️⃣ Librerías necesarias
```bash
pip install sentence-transformers torch transformers qdrant-client==1.15.5
pip install langchain==1.0.5 langchain-core==1.0.4 langchain-huggingface langchain-qdrant langchain-ollama>=1.0.0
pip install fastapi uvicorn  # Opcional para servir API
```

> ⚠️ Notas sobre versiones:  
> - **Qdrant-client >= 1.15.1**: Soluciona errores con `update_collection` y `hnsw_config`.  
> - **LangChain 1.0+**: Cambios en integración con Ollama. La clase `Ollama` antigua está deprecada; usar `OllamaLLM`.

### 3️⃣ Qdrant

#### Local:
```bash
docker run -p 6333:6333 qdrant/qdrant
```
Verifica que esté activo en: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

#### Nube:
1. Crea una cuenta en [Qdrant Cloud](https://cloud.qdrant.io).  
2. Crea un cluster gratuito.  
3. Obtén tu API Key y endpoint.

---

## Estructura del código

### 1️⃣ Embeddings
```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

### 2️⃣ Conexión con Qdrant
```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
collection_name = "docs_vectorialesv2"
```

### 3️⃣ VectorStore
```python
from langchain_qdrant import QdrantVectorStore

vectorstore = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings,
    content_payload_key="texto"  # clave usada para recuperar texto
)
```

### 4️⃣ Retriever
```python
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

test_query = "instrumentos para medir la atmósfera"
results = retriever.invoke(test_query)

for r in results:
    print(r.page_content)
```

> El **retriever** busca los vectores más cercanos al embedding de la consulta.  
> `r.page_content` muestra el texto original almacenado en Qdrant.

### 5️⃣ Modelo LLM
```python
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3", temperature=0)
```

> 🔹 `temperature=0`: respuestas determinísticas; valores mayores generan respuestas más creativas.

### 6️⃣ Prompt y RAG moderno
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

prompt = ChatPromptTemplate.from_template("""
Usa el siguiente contexto para responder la pregunta de manera concisa.
Si no hay información suficiente, responde que no lo sabes.

Contexto:
{context}

Pregunta:
{question}
""")

rag_chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | llm
)

query = "¿Qué sistema se usa para analizar datos atmosféricos?"
respuesta = rag_chain.invoke(query)
print(respuesta)
```

> La **cadena RAG** combina la recuperación de contexto con el LLM para generar respuestas basadas en información existente.

---

## Probando la base de datos

```python
points = [
    {"id": 1, "vector": embedding, "payload": {"texto": "Datos sobre la atmósfera"}}
]

vectorstore.upsert(points)
```

- Puedes actualizar o añadir información a una **colección existente**; los datos se insertan o actualizan automáticamente.  
- Para verificar los contenidos:

```python
for doc in vectorstore.get_all():
    print(doc)
```

---

## Notas importantes de versiones

| Componente | Versión usada | Problemas conocidos en versiones antiguas |
|------------|---------------|-----------------------------------------|
| Qdrant-client | 1.15.5 | `update_collection` fallaba con `hnsw_config.ef_search` |
| LangChain | 1.0.5 | Integración antigua de Ollama deprecada (`Ollama` vs `OllamaLLM`) |
| LangChain Ollama | >=1.0.0 | Necesario para usar `OllamaLLM` moderno |
| SentenceTransformers | 5.1.2 | Compatible con PyTorch 2.9 y transformers 4.57 |
| PyTorch | 2.9.0 | - |

> Con estas versiones, el **código presentado es funcional** y evita errores de deprecación o incompatibilidad.

---

## Resumen

- Mini sistema **RAG completo**: textos → embeddings → Qdrant → LangChain → LLM → respuesta.  
- La colección vectorial puede ser **actualizada y ampliada** sin problemas.  
- El sistema es reproducible localmente o en la nube.  
- Funciona con **LangChain moderno** y Ollama **sin depender de clases deprecadas**.