from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_community.embeddings import HuggingFaceEmbeddings

def load_embedder():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")