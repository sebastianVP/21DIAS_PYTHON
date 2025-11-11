from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
#----- Configuracion Inicial---------
load_dotenv()
API_QDRANTIO = os.getenv("API_QDRANTIO")

qdrant_client = QdrantClient(
    url="https://ba81c210-b95d-4997-b3be-cea480698fc4.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key=API_QDRANTIO,
)

print(qdrant_client.get_collections())
# COMO SE IMPRIME UNA LISTA VACIA ESTAMOS CONECTADOS :)