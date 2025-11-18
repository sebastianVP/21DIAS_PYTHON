# -----------------------------------------------------------
# Script: insertar_cintilaciones_langchain_ollama.py
# Autor: Alexander Valdez
# Objetivo: Insertar definiciones de cintilaciones en Qdrant
#           usando LangChain + OllamaEmbeddings
# -----------------------------------------------------------

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from dotenv import load_dotenv
import os
import uuid

# ------------------ Configuración ------------------

load_dotenv()
API_QDRANTIO = os.getenv("API_QDRANTIO")

qdrant = QdrantClient(
    url="https://ba81c210-b95d-4997-b3be-cea480698fc4.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key=API_QDRANTIO
)

# Modelo para embeddings en Ollama
embedder = OllamaEmbeddings(model="llama3")

# ------------------ Datos a insertar ------------------

definiciones = [
    "La cintilación ionosférica es la variación rápida en amplitud y fase que afecta a señales GNSS al atravesar plasma irregular en la ionosfera.",
    "Los eventos de cintilación suelen estar asociados a burbujas ecuatoriales generadas tras la puesta del sol.",
    "El índice S4 mide la fluctuación en amplitud de una señal GNSS causada por irregularidades ionosféricas.",
    "El índice sigma phi cuantifica las variaciones de fase durante un evento de cintilación ionosférica.",
    "Las regiones cercanas al ecuador magnético presentan mayor ocurrencia de cintilaciones.",
    "Las cintilaciones pueden causar pérdidas de seguimiento en receptores GNSS.",
    "Los radares ionosféricos permiten observar irregularidades de plasma que generan cintilaciones.",
    "Las señales de baja frecuencia tienden a ser más afectadas por las cintilaciones ionosféricas.",
    "La actividad geomagnética elevada puede intensificar los eventos de cintilación.",
    "Los modelos predictivos buscan anticipar la aparición de irregularidades que generen cintilaciones en GNSS."
]

# ------------------ Crear colección ------------------

print("Generando embedding de ejemplo para definir tamaño del vector...")

ejemplo_vector = embedder.embed_query("cintilación ionosférica")
vec_dim = len(ejemplo_vector)

print(f"Tamaño del embedding: {vec_dim}")

print("Creando colección 'cintilaciones'...")

qdrant.recreate_collection(
    collection_name="cintilaciones",
    vectors_config=VectorParams(
        size=vec_dim,
        distance=Distance.COSINE
    )
)

print("Colección creada exitosamente.")

# ------------------ Insertar embeddings ------------------

puntos = []

print("Generando embeddings e insertando puntos en Qdrant...")

for texto in definiciones:
    vector = embedder.embed_query(texto)

    punto = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "descripcion": texto,
            "categoria": "cintilacion",
            "modelo_embeddings": "llama3.1"
        }
    )

    puntos.append(punto)

qdrant.upsert(
    collection_name="cintilaciones",
    points=puntos,
    wait=True
)

print("✔ Inserción completada: 10 definiciones añadidas exitosamente.")
