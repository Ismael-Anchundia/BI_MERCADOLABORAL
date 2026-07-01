import os
import sys
import time
from playwright.sync_api import sync_playwright

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from utils.helpers import guardar_json

# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_URL = "https://www.multitrabajos.com"

SEARCH_URL = f"{BASE_URL}/api/avisos/searchV2?pageSize=20&page=0&sort=RELEVANTES"
DETAIL_URL = f"{BASE_URL}/api/candidates/fichaAvisoNormalizada"

QUERY = "software"
PAGE_SIZE = 20


# ============================================================
# OBTENER OFERTAS
# ============================================================

def obtener_ofertas(page):
    pagina = 0
    ofertas = []

    while True:
        print(f"Descargando página {pagina + 1}...")

        url = f"{BASE_URL}/api/avisos/searchV2?pageSize={PAGE_SIZE}&page={pagina}&sort=RELEVANTES"

        try:
            response = page.request.post(
                url,
                data={
                    "filtros": [],
                    "query": QUERY
                }
            )

            if response.status != 200:
                print(f"Error HTTP {response.status}")
                break

            datos = response.json()
            contenido = datos.get("content", [])

            if not contenido:
                break

            ofertas.extend(contenido)
            pagina += 1

            time.sleep(1)

        except Exception as e:
            print("Error al consultar Multitrabajos:", e)
            break

    return ofertas


# ============================================================
# OBTENER DETALLE
# ============================================================

def obtener_detalle(page, id_aviso):
    response = page.request.get(
        f"{DETAIL_URL}/{id_aviso}"
    )

    if response.status != 200:
        raise Exception(f"HTTP {response.status}")

    return response.json()


# ============================================================
# EXTRAER DETALLES
# ============================================================

def extraer_ofertas(page, ofertas):
    datos = []
    total = len(ofertas)

    for i, oferta in enumerate(ofertas, start=1):
        id_aviso = oferta.get("id")

        print(f"[{i}/{total}] Oferta {id_aviso}")

        try:
            detalle = obtener_detalle(page, id_aviso)
            datos.append(detalle)

        except Exception as e:
            print(f"Error con {id_aviso}: {e}")

        time.sleep(1)

    return datos


# ============================================================
# MAIN
# ============================================================

def main():

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)
            context = browser.new_context()

            page = context.new_page()

            # 🔥 IMPORTANTE: cargar la web primero para generar cookies
            page.goto(BASE_URL, wait_until="networkidle")

            print("Buscando ofertas...")

            ofertas = obtener_ofertas(page)

            print(f"Ofertas encontradas: {len(ofertas)}")

            print("Descargando detalles...")

            datos = extraer_ofertas(page, ofertas)

            archivo = guardar_json(
                datos,
                "data/raw/scraping/multitrabajos",
                "multitrabajos"
            )

            print(f"Detalles descargados: {len(datos)}")
            print(f"Archivo generado: {archivo}")

            browser.close()

    except Exception as e:
        print("Error general:", e)


if __name__ == "__main__":
    main()