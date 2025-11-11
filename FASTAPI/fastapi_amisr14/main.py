"""
ejecucion: uvicorn main:app --reload

curl -X POST "http://127.0.0.1:8000/medicion/" -H "Content-Type: application/json" -d '{"estacion": "AMISR14", "frecuencia_mhz": 450.0, "potencia_kW": 155.5, "timestamp": "2025-11-03T13:45:00", "temperatura_c": 25.0}'

# VER MEDICIONES
curl http://127.0.0.1:8000/mediciones/
"""
from fastapi import FastAPI
from models import RadarMedicion
from typing import List
import asyncio
import json
from datetime import datetime

app = FastAPI(title="API Radar AMISR 14 -IGP")

# base temporal de datos- LISTA TEMPORAL DE DATOS SE VACIA CADA VEZ QUE REINICIAMOS
RADAR_DATA=[]

@app.post("/medicion/")
async def recibir_medicion(data: RadarMedicion):
    """
    Recibe datos de radar simulando un retaro  de red o procesamiento.
    """
    await asyncio.sleep(1.5) # simular retardo de transmision
    RADAR_DATA.append(data.dict())
    # opcional :guardar en archivo
    with open("data/radar_data.json","w") as f:
        json.dump(RADAR_DATA,f,indent=4,default=str)
    return {"status":"ok","mensaje":f"Medicion de {data.estacion} recibida"}

@app.get("/mediciones/",response_model=List[RadarMedicion])
def listar_mediciones():
    """Devuelve todas las mediciones registradas"""
    return RADAR_DATA

@app.get("/estado/")
def estado():
    return {
        "sistema":"AMISR14",
        "ubicacion":"Jicamarca, Lima-Peru",
        "total_mediciones":len(RADAR_DATA),
        "ultima_actualizacion":datetime.now().isoformat()
    }