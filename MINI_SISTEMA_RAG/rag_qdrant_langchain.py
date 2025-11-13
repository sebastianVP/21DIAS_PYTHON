"""
Objetivo: Conectar base vectorial (Qdrant) con un modelo LLM para responder con contexto.

pip install -U langchain-community langchain-core langchain-ollama langchain-text-splitters qdrant-client sentence-transformers

Usar la versión moderna (LangChain 1.0+)

La clase RetrievalQA fue reemplazada por el pipeline de Runnables.

Así se implementa ahora un RAG moderno con tu setup actual (langchain==1.0.5 + langchain-community + langchain-ollama):

"""

# rag_qdrant_langchain.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from qdrant_client import QdrantClient

# 1️⃣ Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2️⃣ Conexión al cliente Qdrant
client = QdrantClient(url="http://localhost:6333")

collection_name="docs_vectorialesv2"

# 2.5 Verificar si la colección existe
collections = client.get_collections().collections
nombres = [c.name for c in collections]

print(f"📦 Colecciones existentes en Qdrant: {nombres}")

if collection_name not in nombres:
    print(f"⚠️ La colección '{collection_name}' NO existe. Se creará automáticamente al agregar datos.")
else:
    print(f"✅ La colección '{collection_name}' ya existe.")

# 3️⃣ Vector store (la colección debe existir o se crea automáticamente)

try:
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
        content_payload_key="texto"  # 👈 clave correcta en tu Qdrant por default es "page_content"
    )
    print(f"✅ VectorStore creado correctamente para la colección: {collection_name}")
except Exception as e:
    print(f"❌ Error al crear el VectorStore: {e}")


# 4 Probar recuperación de contexto
try:
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    test_query = "instrumentos para medir la atmósfera"
    results = retriever.invoke(test_query)
    print("\n🔎 Resultados de recuperación:")
    if not results:
        print("⚠️ No se recuperaron documentos similares.")
    else:
        for i, r in enumerate(results):
            print(f"Documento {i+1}: {r.page_content}...")
except Exception as e:
    print(f"❌ Error al recuperar datos: {e}")

# 5️⃣ Modelo LLM
llm = OllamaLLM(model="llama3", temperature=0)

# 6️⃣ Prompt
prompt = ChatPromptTemplate.from_template("""
Usa el siguiente contexto para responder la pregunta de manera concisa.
Si no hay información suficiente, responde que no lo sabes.

Contexto:
{context}

Pregunta:
{question}
""")

# 7️⃣ Cadena RAG moderna
rag_chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | llm
)

# 8️⃣ Prueba
query = "\n¿Qué instrumentos se usa para medir la atmosfera?"
respuesta = rag_chain.invoke(query)
print(query)
print("-------------------------------")
print("\n🧠 Respuesta del modelo:")
print(respuesta)
