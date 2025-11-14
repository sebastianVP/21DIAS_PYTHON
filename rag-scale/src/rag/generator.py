from langchain_community.llms import Ollama

def load_llm():
    return Ollama(
        model="llama3",
        temperature=0.0,
    )