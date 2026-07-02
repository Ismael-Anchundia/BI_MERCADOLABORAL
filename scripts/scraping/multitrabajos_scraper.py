import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from utils.helpers import guardar_json


BASE_URL = "https://www.multitrabajos.com"
SEARCH_PAGE = "https://www.multitrabajos.com/empleos-busqueda-software.html"

QUERY = "software"
PAGE_SIZE = 20
MAX_PAGES = 3


def buscar_respuesta_api(page, pagina):
    url_api = f"{BASE_URL}/api/avisos/searchV2?pageSize={PAGE_SIZE}&page={pagina}&sort=RELEVANTES"

    print(f"Consultando Multitrabajos página {pagina + 1}...")

    response = page.evaluate(
        """
        async ({urlApi, query}) => {
            const response = await fetch(urlApi, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "x-site-id": "BMEC"
                },
                body: JSON.stringify({
                    filtros: [],
                    query: query
                })
            });

            const text = await response.text();

            return {
                status: response.status,
                text: text
            };
        }
        """,
        {
            "urlApi": url_api,
            "query": QUERY
        }
    )

    if response["status"] != 200:
        raise Exception(f"HTTP {response['status']} - {response['text'][:300]}")

    return json.loads(response["text"])


def extraer_todas_las_ofertas(page):
    datos_totales = []

    for pagina in range(MAX_PAGES):
        try:
            datos = buscar_respuesta_api(page, pagina)

            contenido = datos.get("content", [])

            print(f"Ofertas detectadas en página {pagina + 1}: {len(contenido)}")

            if not contenido:
                break

            datos_totales.extend(contenido)

            total = datos.get("total", 0)
            acumulado = len(datos_totales)

            if acumulado >= total:
                break

            time.sleep(1)

        except Exception as e:
            print(f"Error en página {pagina + 1}: {e}")
            break

    return datos_totales


def main():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1366, "height": 768},
                locale="es-EC"
            )

            page = context.new_page()

            print("Abriendo Multitrabajos...")
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)
            time.sleep(4)

            print("Abriendo búsqueda de software...")
            page.goto(SEARCH_PAGE, wait_until="domcontentloaded", timeout=60000)
            time.sleep(5)

            
            datos = extraer_todas_las_ofertas(page)

            archivo = guardar_json(
                datos,
                "data/raw/scraping/multitrabajos",
                "multitrabajos"
            )

            print(f"Total ofertas guardadas: {len(datos)}")
            print(f"Archivo generado: {archivo}")

            browser.close()

    except Exception as e:
        print("Error general:", e)


if __name__ == "__main__":
    main()