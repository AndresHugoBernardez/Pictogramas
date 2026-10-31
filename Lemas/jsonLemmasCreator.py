
import json
from pathlib import Path

# Archivos
archivo_entrada = Path("lemmatization-es.txt")
archivo_diccionario = Path("dictLemmas.json")
archivo_variantes = Path("varLemmas.json")

# Diccionarios
diccionario = {}
variantes = {}

# Estadísticas
lineas_procesadas = 0
errores = 0

# Leer archivo
with archivo_entrada.open("r", encoding="utf-8") as archivo:
    for numero_linea, linea in enumerate(archivo, 1):

        linea = linea.strip()

        if not linea:
            continue

        partes = linea.split(maxsplit=1)

        if len(partes) != 2:
            print(f"Error en línea {numero_linea}: {linea}")
            errores += 1
            continue

        lema, palabra = partes

        # Índice palabra -> lema
        diccionario[palabra] = lema

        # Índice lema -> palabras
        if lema not in variantes:
            variantes[lema] = []

        if palabra not in variantes[lema]:
            variantes[lema].append(palabra)

        lineas_procesadas += 1


# Guardar JSON palabra -> lema
with archivo_diccionario.open("w", encoding="utf-8") as archivo:
    json.dump(
        diccionario,
        archivo,
        ensure_ascii=False,
        indent=2
    )


# Guardar JSON lema -> palabras
with archivo_variantes.open("w", encoding="utf-8") as archivo:
    json.dump(
        variantes,
        archivo,
        ensure_ascii=False,
        indent=2
    )


# Resultado
print("Proceso finalizado.")
print(f"Líneas procesadas: {lineas_procesadas}")
print(f"Palabras únicas: {len(diccionario)}")
print(f"Lemas únicos: {len(variantes)}")
print(f"Errores: {errores}")
print(f"Archivo creado: {archivo_diccionario}")
print(f"Archivo creado: {archivo_variantes}")