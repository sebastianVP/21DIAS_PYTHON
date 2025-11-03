import asyncio
import random
import time
# ---- Simulacionde  3 sensores indivuadeles

async def sensor(nombre:str,rango:tuple[float,float],intervalo:tuple[int,int])->None:
    for _ in range(3): #cada sensor envia 3 lecturas
        await asyncio.sleep(random.uniform(*intervalo)) # retardo aleatorio
        lectura =  round(random.uniform(*rango),2)
        print(f"[{time.strftime("%H:%M:%s")}] {nombre}->{lectura}")

async def main():
    print("===Iniciando Lectura asincrona de sensores===")
    inicio = time.time()
    # EJECUTAMOS TODOS LOS SENSORES SIMULTANEAMENT
    await asyncio.gather(
        sensor("Temperatura(°C)",(18.0,30.0),(0.5,2.0) ),
        sensor("Humedad (%)",(40-0,90.0),(1.0,3.0)),
        sensor("Presion(hPa)",(900.0,1100.0),(0.2,1.5))
    )
    fin =time.time()
    print(f"\n Lectura completada en{fin-inicio:.2f} segundos") 

# Ejecutamos el bucle principal
asyncio.run(main())