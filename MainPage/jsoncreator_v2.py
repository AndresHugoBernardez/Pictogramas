
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

# palabra -> lista de códigos Unicode sin duplicados
mapa_pictogramas = {}

# Sintagma completo -> código Unicode
mapa_sintagmas = {}


def normalizar(texto):
    return texto.strip().lower()


with open("mapa_pictogramas.csv", mode="r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        nombre = normalizar(row["nombre"])
        codigo = row["codigo_unicode"][2:] 

        if not nombre or not codigo:
            continue

        # Guarda también el sintagma completo.
        if nombre not in mapa_sintagmas:
            mapa_sintagmas[nombre] = []

        if codigo not in mapa_sintagmas[nombre]:
            mapa_sintagmas[nombre].append(codigo)

        # Divide el sintagma en palabras y elimina puntuación.
        palabras = re.findall(r"[^\W_]+", nombre, flags=re.UNICODE)

        for palabra in palabras:
            if palabra in conectores:
                continue

            if palabra not in mapa_pictogramas:
                mapa_pictogramas[palabra] = []

            if codigo not in mapa_pictogramas[palabra]:
                mapa_pictogramas[palabra].append(codigo)





with open("sclera_map.json", "w", encoding="utf-8") as f:
    json.dump(mapa_pictogramas, f, ensure_ascii=False, indent=2)
with open("sclera_sintagmas_map.json", "w", encoding="utf-8") as f:
    json.dump(mapa_sintagmas, f, ensure_ascii=False, indent=2)

print("¡JSONs de la fuente creado con éxito!")
print(f"Palabras indexadas: {len(mapa_pictogramas)}")
print(f"Sintagmas registrados: {len(mapa_sintagmas)}")