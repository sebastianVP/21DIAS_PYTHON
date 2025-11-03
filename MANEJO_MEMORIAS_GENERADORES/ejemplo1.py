"""
MANEJO DE MEMORIA Y GENERADORES
Pytho usa recoleccion de basura 
"""
import sys
def generador():
    for i in range(10_000_00):
        yield i # generar sin cargar todo en memoria
g= generador()
print(sys.getsizeof(g)) #muy pequeño
a= list(range(10_000_000))
print(sys.getsizeof(a)) 

