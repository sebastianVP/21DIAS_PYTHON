"""
Type Hints (Tipado Estático en Python)

Los type hints ayudan a detectar errores antes de ejecutar.
🧩 Qué revisa mypy

Tipos de argumentos y valores retornados.

Variables con tipos anotados.

Compatibilidad entre clases e interfaces.

Uso correcto de tipos genéricos (por ejemplo list[str], dict[int, float], etc.).

Errores sutiles que no se detectan hasta que el programa falla.

mypy ejemplo1.py
"""
#def sumar(a:int,b:int)->int:
#    return a+b

def procesar_datos(datos:list[str])->dict[str,int]:
    return {d: len(d) for d in datos}