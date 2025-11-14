"""
pip show langchain-ollama
si no sale el paquete
pip install -U langchain-ollama


"""
# test_ollama.py
from langchain_community.llms import Ollama

# Verificación del modelo
llm = Ollama(model="llama3", temperature=0)

print("✅ Ollama cargado correctamente con LangChain Community")
print("🧠 Probando generación...")

#respuesta = llm.invoke("¿Cuál es la capital de Perú?")
respuesta = llm.invoke("¿Alan Garcia dio un discurso en el 2008?")

print("💬 Respuesta:", respuesta)