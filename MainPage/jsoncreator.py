import csv
import json

# Mapa para almacenar: {"palabra": ["\uE001", "\uE002"]}
mapa_pictogramas = {}

with open('mapa_pictogramas.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Tomamos el nombre/tag y nos quedamos con la primera palabra
        tag_completo = row['nombre'].strip().lower()
        tag_principal = tag_completo.split()[0]  # Solo la primera palabra
        
        unicode_char = row['codigo_unicode'][2:] # Ej: "\uE001" o el código correspondiente

        if tag_principal not in mapa_pictogramas:
            mapa_pictogramas[tag_principal] = []
        
        # Agregamos el carácter si no está repetido
        if unicode_char not in mapa_pictogramas[tag_principal]:
            mapa_pictogramas[tag_principal].append(unicode_char)

# Guardamos el JSON de la fuente listo para la web
with open('sclera_map.json', 'w', encoding='utf-8') as f:
    json.dump(mapa_pictogramas, f, ensure_ascii=False, indent=2)

print("¡JSON de la fuente creado con éxito!")
