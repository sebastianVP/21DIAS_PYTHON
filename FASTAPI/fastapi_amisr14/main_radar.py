"""
🚀 Objetivo

Transformar tu API FastAPI para:
Guardar cada medición en una colección MongoDB (p. ej. mediciones_radar).
Permitir listar las mediciones desde MongoDB.
Mantener compatibilidad con tu estructura actual (RadarMedicion).

ENDPOINT: En una API, un endpoint (o “punto final”) es una URL específica que permite enviar o recibir información.

👉 En otras palabras, es una dirección dentro del servidor a la cual un cliente (como Postman, curl o tu dashboard web) puede hacer una solicitud.
EJECUCION:
$ uvicorn main_radar:app --reload
post:
curl -X POST "http://127.0.0.1:8000/medicion/" \
-H "Content-Type: application/json" \
-d '{"estacion": "AMISR14", "frecuencia_mhz": 450.0, "potencia_kW": 155.5, "timestamp": "2025-11-03T13:45:00", "temperatura_c": 25.0}'

"""
from fastapi import FastAPI
from models import RadarMedicion
from typing import List
from datetime import datetime
import motor.motor_asyncio
import os
from dotenv import load_dotenv
#----- Configuracion Inicial---------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME   = os.getenv("DB_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db= client[DB_NAME]
collection =  db["mediciones_radar"]

app= FastAPI(title="API Rdar AMISR14-IGP")


# --ENDPOINT: POST /medicion/ --
@app.post("/medicion/")
async def recibir_mediciones(data: RadarMedicion):
    """Recibe y almacena una medicion de radar"""
    doc= data.dict()
    doc["timestamp_insertado"]=datetime.now()
    await collection.insert_one(doc)
    return {"status":"ok","mensaje":f"Medicion de {data.estacion} guardada en MongoDB"}

# --ENDPOINT: GET /mediciones/--
@app.get("/mediciones/",response_model=List[RadarMedicion])
async def listar_mediciones():
    """Devuelve todas la mediciones desde MongoDB"""
    mediciones  = await collection.find().to_list(1000)
    return mediciones


# --- ENDPOINT: GET /estado/
@app.get("/estado/")
async def estado():
    total = await collection.count_documents({})
    ultima = await collection.find().sort("timestamp_insertado",-1).to_list(1)
    ultima_fecha = ultima[0]["timestamp_insertado"].isoformat() if ultima else None
    return {
        "sistema":"AMISR14",
        "ubicacion":"Jicamarca,Lima-Peru",
        "total_mediciones":total,
        "ultima_actualizacion":ultima_fecha,
    }