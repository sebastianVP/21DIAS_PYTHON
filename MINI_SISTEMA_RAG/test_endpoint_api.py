"""
✅ Beneficios de este enfoque

Tu pipeline RAG ya está en producción local o nube.

Permite recibir preguntas vía HTTP y devolver respuestas generadas.

Puedes escalar añadiendo más colecciones o conectando otros LLM.

Fácil integración con frontends o bots.
"""
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "¿Qué instrumentos se usan para medir la atmósfera?"}
)
print(response.json())