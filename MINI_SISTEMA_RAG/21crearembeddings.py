from sentence_transformers import SentenceTransformer
# para cargar el uso de cuda
import torch
torch.cuda.empty_cache()
print(torch.cuda.get_device_name(0))
print(f"Memoria GPU libre: {torch.cuda.mem_get_info()[0]/1024**2:.2f} MB")
# comando para revisar procesos que estan ocupando el cuda


model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "El radar mide la reflectividad de las precipitaciones.",
    "La ionosfera afecta las señales GPS.",
    "El modelo LSTM se usa para series temporales.",
    "Qdrant permite búsquedas semánticas rápidas."
]

vectors = model.encode(texts)
print("vectors shape:",vectors.shape)
