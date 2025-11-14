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
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


class QueryRequest(BaseModel):
    question: str

app = FastAPI()
db = init_vector_collection_ready_db()

retriever = get_retriever(db)
llm = load_llm()

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

rag_chain = (
RunnableParallel({"context":retriever,"question":RunnablePassthrough()})
| prompt
| llm
)

@app.post("/ask")
def ask_question(request:QueryRequest):
    try:
        respuesta = rag_chain.invoke(request.question)
        return {"question":request.question,"answer":respuesta}
    except Exception as e:
        return {"error":str(e)}
    