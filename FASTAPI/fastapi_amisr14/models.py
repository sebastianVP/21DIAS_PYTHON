from pydantic import BaseModel
from datetime import datetime

class RadarMedicion(BaseModel):
    estacion: str
    frecuencia_mhz:float
    potencia_kW: float
    timestamp: datetime
    temperatura_c:float
    