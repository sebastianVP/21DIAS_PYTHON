"""
Ejecucion:
1. Instala dependencias
pip install -r requirements.txt

2. Levanta Qdrant
docker run -p 6333:6333 qdrant/qdrant

3. Ingresa los PDFs
python src/ingest/pipeline_ingest.py

4. Genera embeddings y carga en Qdrant (te doy script si lo deseas)
5. Inicia el API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000


"""

from fastapi import FastAPI
from src.rag.generator import load_llm
from src.rag.retriever import get_retriever
from src.embeddings.vector_store import init_vector_db,init_vector_collection_ready_db
from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str

app = FastAPI()
db = init_vector_collection_ready_db()

retriever = get_retriever(db)
llm = load_llm()

@app.post("/ask")
def ask_question(request:QueryRequest):
    query= request.question
    docs = retriever.invoke(query)
    context = "\n".join([d.page_content for d in docs])

    prompt = f"Contexto:\n{context}\n\nPregunta: {query}\nRespuesta:"
    answer = llm.invoke(prompt)

    return {"answer": answer}