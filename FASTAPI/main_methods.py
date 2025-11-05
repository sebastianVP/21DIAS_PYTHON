"""
Comprendiendo los metodos:
- GET,POST,PUT Y DELETE
Objetivo: Entender como FastAPI asocia cada método HTTP a una función Python y 
como enviar/recibir datos

Comando de ejecucion:
uvicorn main_methods:app --reload
sudo apt install uvicorn
*Agregar un sensor:
curl -X POST "http://127.0.0.1:8000/sensores/" -H "Content-Type: application/json" -d "{\"id\":3,\"nombre\":\"RDR_TEST\",\"ubicacion\":\"Arequipa\"}"
*Actualizar un sensor
curl -X PUT "http://127.0.0.1:8000/sensores/3" -H "Content-Type: application/json" -d "{\"id\":3,\"nombre\":\"RDR_TEST\",\"ubicacion\":\"Cusco\"}"
*Eliminarlo
curl -X DELETE "http://127.0.0.1:8000/sensores/3"

"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Demo Metodos FastAPI")

# Modelos de datos(esta es una estructura de datos)
class Sensor(BaseModel):
    id        : int
    nombre    : str
    ubicacion : str

# Base Simulada
sensores = {
    1 : {"id":1,"nombre":"AMISR14","ubicacion":"Jicamarca"},
    2 : {"id":2,"nombre":"ESF01","ubicacion":"Piura"}
}

# 1 GET-Leer Informaion
@app.get("/sensores/")
def listar_sensores():
    return list(sensores.values())

# 2 GET con parametro-> obtener un sensor especifico
@app.get("/sensores/{sensor_id}")
def obtener_sensor(sensor_id:int):
    return sensores.get(sensor_id,{"error":"Sensor no encontrado"})

# 3 POST-> Crear un nuevo sensor
@app.post("/sensores/")
def agregar_sensor(sensor:Sensor):
    sensores[sensor.id] = sensor.dict()
    return {"mensaje":"Sensor agregado","sensor":sensor}

#  4 PUT - Actualizar sensor
@app.put("/sensores/{sensor_id}")
def actualizar_sensor(sensor_id:int,sensor:Sensor):
    if sensor_id in sensores:
        sensores[sensor.id]=sensor.dict()
        return {"mensaje":"Sensor actualizado","sensor":sensor}
    
# 5 DELETE - Eliminar Sensor
@app.delete("/sensores/{sensor_id}")
def elimiar_sensor(sensor_id:int):
    if sensor_id in sensores:
        del sensores[sensor_id]
        return {"mensaje":f"Sensor {sensor_id} eliminado"}
    return {"error":"Sensor no encontrado"}