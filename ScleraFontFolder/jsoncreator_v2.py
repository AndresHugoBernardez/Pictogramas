import csv
import json
import re
import unicodedata

# Palabras que no identifican por sí solas un pictograma.
# Podés ampliar esta lista según las necesidades de tu diccionario.
conectores = {
    "a", "al", "de", "del", "el", "la", "las", "lo", "los",
    "un", "una", "unos", "unas",
    "y", "e", "o", "u", "ni",
    "con", "sin", "en", "por", "para", "desde", "hasta",
    "sobre", "entre", "hacia", "contra", "ante", "bajo",
    "tras", "durante", "mediante",
    "que", "se"
}

#Numeros
numeros = {
"0","1","2","3","4","5","6","7","9","0"
}

# palabra -> lista de códigos Unicode sin duplicados
mapa_pictogramas = {}

# Sintagma completo -> código Unicode
mapa_sintagmas = {}


def normalizar(texto):
    return texto.strip().lower()


with open("mapa_pictogramas.csv", mode="r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        tag=row["nombre"]
        nombre = normalizar(tag)
        codigo = row["codigo_unicode"][2:] 

        if not nombre or not codigo:
            continue

         # Limpiar sufijos numéricos al final del nombre (ej: '_1', ' 1', '_02', etc.)
        nombre = re.sub(r'[\s_]+\d+$', '', nombre).strip()

        # 1. Guarda en mapa_sintagmas con la estructura {"codigos": [...], "tags": [...]}
        if " " in nombre:
            if nombre not in mapa_sintagmas:
                mapa_sintagmas[nombre] = {
                    "codigos": [],
                    "tags": []
                }
            if codigo not in mapa_sintagmas[nombre]["codigos"]:
                mapa_sintagmas[nombre]["codigos"].append(codigo)
                mapa_sintagmas[nombre]["tags"].append(tag)

        # Si el nombre completo es un conector,
        # se conserva como una palabra indexable.
        if nombre in conectores:
            palabras = [nombre]
        else:
            # Divide el sintagma en palabras y elimina puntuación.
            palabras = re.findall(r"[^\W_]+", nombre, flags=re.UNICODE)

            # Excluye los conectores únicamente dentro de sintagmas.
            palabras = [p for p in palabras if p not in conectores]

        # 2. Guarda en mapa_pictogramas con la misma estructura
        for palabra in palabras:
            if palabra not in mapa_pictogramas:
                mapa_pictogramas[palabra] = {
                    "codigos": [],
                    "tags": []
                }

            if codigo not in mapa_pictogramas[palabra]["codigos"]:
                mapa_pictogramas[palabra]["codigos"].append(codigo)
                mapa_pictogramas[palabra]["tags"].append(tag)


with open("sclera_map.json", "w", encoding="utf-8") as f:
    json.dump(mapa_pictogramas, f, ensure_ascii=False, indent=2)
with open("sclera_sintagmas_map.json", "w", encoding="utf-8") as f:
    json.dump(mapa_sintagmas, f, ensure_ascii=False, indent=2)

print("¡JSONs de la fuente creado con éxito!")
print(f"Palabras indexadas: {len(mapa_pictogramas)}")
print(f"Sintagmas registrados: {len(mapa_sintagmas)}")