"""
Objetivo: practicar cómo FastAPI consulta otra API del mundo real, 
procesa su respuesta, y la devuelve formateada.
Ejecución:
uvicorn main_external_api:app --reload

"""
from fastapi import FastAPI
import requests
app= FastAPI(title="Demo COnsumo de API Externa- OpenMeteo")

@app.get("/clima/")
def obtener_clima(lat:float =-12.05, lon: float = -76.97):
    """
    Consulta condiciones climaticas reales desde Open-Meteo
    Ejemplo: /clima/?lat=-12.05&lon=-76.97 (Jicamarcaa)
    """
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
    r   = requests.get(url)
    data = r.json()
    print(data)
    clima = {
        "ubicacion":{"lat":lat,"lon":lon},
        "temperatura":data["current"]["temperature_2m"],
        "viento":data["current"]["wind_speed_10m"],
        "fuente":"open-meteo.com"
    }
    return clima
