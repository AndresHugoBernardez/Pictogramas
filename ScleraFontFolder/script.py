import os
import csv
import re
import traceback
import xml.etree.ElementTree as ET
import fontforge

# =========================================================
# CONFIGURACION
# =========================================================


CARPETA = r"C:\Users\Andrux\Downloads\ScleraPictos"

CARPETA_SVG = os.path.join(CARPETA, "SVG_Potrace_800")
CARPETA_SVG_LIMPIOS = os.path.join(CARPETA, "_SVG_limpios")
CARPETA_SALIDA = os.path.join(CARPETA, "ScleraFontFolder")

NOMBRE_FUENTE = "ScleraFont"

UNICODE_INICIAL = 0xF0000
UNICODE_FINAL = 0xFFFFD

ANCHO_GLIFO = 1000

# Simplificacion de contornos en unidades de la fuente.
# Si aparecen deformaciones, cambiar a 0 para desactivarla.
SIMPLIFICAR = True
TOLERANCIA = 1.0

# =========================================================
# FUNCIONES
# =========================================================

def limpiar_svg(origen, destino):
    """
    Lee un SVG y crea una copia reducida.
    Conserva grupos y trazados, incluidos sus atributos
    geometricos como transform y d.
    No modifica el SVG original ni vuelve a vectorizarlo.
    """

    arbol = ET.parse(origen)
    raiz_original = arbol.getroot()

    atributos = dict(raiz_original.attrib)

    # Conservar las propiedades geometricas de la raiz.
    raiz = ET.Element(
        "{http://www.w3.org/2000/svg}svg",
        atributos
    )

    # Copiar solo grupos y elementos vectoriales.
    # Los SVG de Potrace normalmente usan g y path.
    permitidos = {
        "g", "path", "rect", "circle", "ellipse",
        "line", "polyline", "polygon", "defs",
        "clipPath", "mask"
    }

    def copiar_elemento(elemento, padre):
        etiqueta = elemento.tag.split("}")[-1]

        if etiqueta not in permitidos:
            return

        nuevo = ET.SubElement(
            padre,
            elemento.tag,
            dict(elemento.attrib)
        )

        nuevo.text = elemento.text
        nuevo.tail = None

        for hijo in list(elemento):
            copiar_elemento(hijo, nuevo)

    for hijo in list(raiz_original):
        copiar_elemento(hijo, raiz)

    # Comprobar que haya trazados con geometria.
    trazados = raiz.findall(".//{*}path")
    validos = [
        p for p in trazados
        if p.get("d", "").strip()
    ]

    if not validos:
        raise ValueError("El SVG no contiene trazados path utilizables.")

    ET.ElementTree(raiz).write(
        destino,
        encoding="utf-8",
        xml_declaration=True
    )

    return len(validos)


def nombre_seguro(nombre):
    nombre = re.sub(r"[^A-Za-z0-9_]", "_", nombre)

    if not nombre or not nombre[0].isalpha():
        nombre = "p_" + nombre

    return nombre


def simplificar_glifo(glifo):
    """
    Simplifica contornos ya importados.
    No modifica el SVG original.
    """

    if not SIMPLIFICAR:
        return

    try:
        glifo.simplify(TOLERANCIA)
    except Exception as e:
        print("  AVISO: no se pudo simplificar:", e)


def contar_contornos(glifo):
    try:
        return len(glifo.foreground)
    except Exception:
        return -1


# =========================================================
# PREPARACION
# =========================================================

os.makedirs(CARPETA_SALIDA, exist_ok=True)
os.makedirs(CARPETA_SVG_LIMPIOS, exist_ok=True)

ruta_log = os.path.join(CARPETA_SALIDA, "errores.txt")
ruta_csv = os.path.join(CARPETA_SALIDA, "mapa_pictogramas.csv")

for ruta in (ruta_log, ruta_csv):
    if os.path.exists(ruta):
        os.remove(ruta)

if not os.path.isdir(CARPETA_SVG):
    raise SystemExit(
        "No existe la carpeta de SVG: " + CARPETA_SVG
    )

archivos = sorted(
    f for f in os.listdir(CARPETA_SVG)
    if f.lower().endswith(".svg")
)

if not archivos:
    raise SystemExit("No se encontraron archivos SVG.")

capacidad = UNICODE_FINAL - UNICODE_INICIAL + 1

if len(archivos) > capacidad:
    raise SystemExit(
        f"Hay {len(archivos)} SVG, pero el rango Unicode "
        f"privado elegido solo admite {capacidad}."
    )

print("SVG encontrados:", len(archivos))
print("Preparando fuente...\n")

# =========================================================
# CREAR FUENTE
# =========================================================

fuente = fontforge.font()
fuente.fontname = NOMBRE_FUENTE
fuente.familyname = NOMBRE_FUENTE
fuente.fullname = NOMBRE_FUENTE
fuente.weight = "Regular"
fuente.em = 1000
fuente.ascent = 800
fuente.descent = 200

notdef = fuente.createChar(-1, ".notdef")
notdef.width = ANCHO_GLIFO

mapa = []
errores = []
exitos = 0
fallidos = 0

# Cada archivo recibe una asignacion estable basada
# en su posicion alfabetica, incluso si otro falla.

for indice, archivo in enumerate(archivos):
    codigo = UNICODE_INICIAL + indice
    ruta_original = os.path.join(CARPETA_SVG, archivo)

    base = os.path.splitext(archivo)[0]
    base_segura = nombre_seguro(base)

    nombre_glifo = f"p_{codigo:04X}_{base_segura}"

    ruta_limpia = os.path.join(
        CARPETA_SVG_LIMPIOS,
        f"{codigo:04X}.svg"
    )

    print(f"[{indice + 1}/{len(archivos)}] {archivo}")

    glifo = None

    try:
        # 1. Simplificar estructura XML sin tocar
        #    los datos geometricos del SVG original.
        numero_trazados = limpiar_svg(
            ruta_original,
            ruta_limpia
        )

        print(f"  Trazados SVG: {numero_trazados}")

        # 2. Crear glifo e importar la copia limpia.
        glifo = fuente.createChar(codigo, nombre_glifo)
        glifo.clear()

        glifo.importOutlines(ruta_limpia)

        # 3. Comprobar si realmente se importaron contornos.
        contornos_antes = contar_contornos(glifo)

        if contornos_antes == 0:
            raise ValueError(
                "FontForge no importo ningun contorno."
            )

        # 4. Simplificar los contornos importados.
        simplificar_glifo(glifo)

        contornos_despues = contar_contornos(glifo)

        # 5. Comprobar que el glifo siga teniendo geometria.
        if contornos_despues == 0:
            raise ValueError(
                "El glifo quedo sin contornos tras simplificar."
            )

        glifo.width = ANCHO_GLIFO

        mapa.append([
            archivo,
            base,
            f"U+{codigo:04X}",
            chr(codigo),
            contornos_despues
        ])

        exitos += 1

        print(
            f"  OK: U+{codigo:04X}; "
            f"contornos: {contornos_despues}"
        )

    except Exception as e:
        fallidos += 1

        mensaje = (
            f"{archivo} | U+{codigo:04X} | "
            f"{type(e).__name__}: {e}"
        )

        errores.append(mensaje)

        print("  ERROR:", mensaje)

        # Eliminar el glifo fallido de la fuente cuando
        # FontForge permita hacerlo.
        if glifo is not None:
            try:
                glifo.clear()
            except Exception:
                pass

        # Guardar detalles adicionales para diagnostico.
        errores.append(traceback.format_exc())

    print()

# =========================================================
# GUARDAR MAPA Y FUENTE
# =========================================================

with open(ruta_csv, "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.writer(f)

    escritor.writerow([
        "archivo_svg",
        "nombre",
        "codigo_unicode",
        "caracter",
        "contornos"
    ])

    escritor.writerows(mapa)

if errores:
    with open(ruta_log, "w", encoding="utf-8") as f:
        f.write("\n".join(errores))

# Guardar fuente editable
ruta_sfd = os.path.join(
    CARPETA_SALIDA,
    NOMBRE_FUENTE + ".sfd"
)

ruta_ttf = os.path.join(
    CARPETA_SALIDA,
    NOMBRE_FUENTE + ".ttf"
)

try:
    fuente.save(ruta_sfd)
    print("SFD guardado:", ruta_sfd)
except Exception as e:
    print("ERROR al guardar SFD:", e)

try:
    fuente.generate(ruta_ttf)
    print("TTF generado:", ruta_ttf)
except Exception as e:
    print("ERROR al generar TTF:", e)

# WOFF y WOFF2 dependen de la compilacion instalada.
for extension in ("woff", "woff2"):
    destino = os.path.join(
        CARPETA_SALIDA,
        NOMBRE_FUENTE + "." + extension
    )

    try:
        fuente.generate(destino)
        print(f"{extension.upper()} generado:", destino)
    except Exception as e:
        print(f"No se pudo generar {extension.upper()}: {e}")

fuente.close()

# =========================================================
# RESUMEN
# =========================================================

print("\n" + "=" * 50)
print("PROCESO TERMINADO")
print("=" * 50)
print("SVG encontrados:", len(archivos))
print("Importaciones correctas:", exitos)
print("Fallidos:", fallidos)
print("Mapa CSV:", ruta_csv)

if errores:
    print("Registro de errores:", ruta_log)

print("Fuente guardada en:", CARPETA_SALIDA)
