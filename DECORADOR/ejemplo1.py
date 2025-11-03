"""
DECORADORES
Un decorador es una funcion que modifica el comportamiento de otra funcion.
Ejemplo visual:

Imagina que la función original es un regalo 🎁
y el decorador le pone un papel bonito y una tarjeta (sin alterar el regalo por dentro).
Ese “papel” es la función wrapper.

Dentro del wrapper, puedes hacer cosas como:

medir el tiempo de ejecución,

registrar logs,

validar argumentos,

o modificar el resultado.
Estructura:
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        # --- código antes de ejecutar la función original ---
        resultado = func(*args, **kwargs)
        # --- código después de ejecutar la función original ---
        return resultado
    return wrapper
"""

import time

def medir_tiempo(func):
    def wrapper(*args,**kwargs):
        inicio    = time.time()
        resultado = func(*args,**kwargs)
        fin       = time.time()
        print(f"{func.__name__} ejecutó en {fin-inicio:.4f} s")
        return resultado
    return wrapper

@medir_tiempo
def procesar_datos():
    time.sleep(2)

procesar_datos()