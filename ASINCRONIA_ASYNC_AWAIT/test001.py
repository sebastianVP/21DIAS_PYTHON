"""
La asincronía permite ejecutar tareas que no bloquean
el flujo principal (por ejemplo, consultas web o lectura de archivos).

Explicación:

async def define una función asincrónica.

await pausa esa tarea sin bloquear las demás.

asyncio.gather() ejecuta varias tareas simultáneamente.
"""
import asyncio

async def tarea(nombre):
    print(f"Inicio {nombre}")
    await asyncio.sleep(2) # simula operacion lenta
    print(f"Fin {nombre}")

async def main():
    await asyncio.gather(
        tarea("Descarga 1"),
        tarea("Desarga 2"),
        tarea("Desarga 3")
    )

asyncio.run(main())