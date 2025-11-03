""""
control de memoria eficiente, una habilidad clave en análisis 
de grandes volúmenes de datos o logs de sensores.

Ejemplo completo y comentado que muestra cómo implementar un generador que
lee un archivo línea por línea sin cargarlo entero en memoria:
"""
def leer_lineas_en_stream(ruta_archivo:str):
    """
    Generado que lee un rachivo linea por linea,
    sin cargarlo completamente en memoria.
    """
    with open(ruta_archivo,"r",encoding="utf-8") as f:
        for linea in f:
            yield linea.strip() ## devolvemos cada linea limpia

ruta= "datos_sensores.txt"
contador =0
for linea in leer_lineas_en_stream(ruta):
    # PROCESAMOS LA LINEA(ejemplo:imprimir las 5 primeras)
    if contador<5:
        print(linea)
    contador +=1
"""
🧠 Qué está pasando aquí

La función leer_lineas_en_stream() no carga el archivo completo en memoria.
En cambio, abre un flujo (with open(...)) y va entregando una línea cada vez
 usando yield.

Cada vez que el bucle for pide una nueva línea, el generador reanuda 
su ejecución justo donde se quedó.

Es ideal para archivos de varios GB, donde una lectura completa
con read() o readlines() saturaría la RAM.

Aplicación práctica

Este patrón se usa mucho para:

Procesamiento de logs o datasets muy grandes.

Lectura de datos de sensores en tiempo real.

Pipelines ETL o tareas de streaming analytics.

"""
# PARA VER LA DIFERENCIA
import sys

ruta = "datos_sensores.txt"

# Versión 1: lectura completa
with open(ruta, "r", encoding="utf-8") as f:
    lineas = f.readlines()
print("Tamaño en memoria (readlines):", sys.getsizeof(lineas), "bytes")

# Versión 2: lectura por generador
g = leer_lineas_en_stream(ruta)
print("Tamaño en memoria (generador):", sys.getsizeof(g), "bytes")