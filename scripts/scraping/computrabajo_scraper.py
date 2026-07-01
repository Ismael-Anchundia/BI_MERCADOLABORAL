import os
import sys
import time
import requests

from bs4 import BeautifulSoup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import HEADERS, TIMEOUT, DELAY
from utils.helpers import guardar_json

# ============================================================
# CONFIGURACIÓN
# ============================================================

URL = "https://ec.computrabajo.com/trabajo-de-software"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

TIMEOUT = 15

# ============================================================
# OBTENER HTML
# ============================================================

def obtener_html():

    respuesta = requests.get(
        URL,
        headers=HEADERS,
        timeout=TIMEOUT
    )

    respuesta.raise_for_status()

    return respuesta.text


# ============================================================
# EXTRAER OFERTAS
# ============================================================

def extraer_ofertas(html):

    soup = BeautifulSoup(html, "html.parser")

    ofertas = soup.find_all("article", class_="box_offer")

    datos = []

    for oferta in ofertas:

        # ------------------------
        # Título
        # ------------------------

        titulo = None

        titulo_tag = oferta.find("a", class_="js-o-link")

        if titulo_tag:
            titulo = titulo_tag.get_text(strip=True)

        # ------------------------
        # Empresa
        # ------------------------

        empresa = None

        empresa_tag = oferta.find("a", class_="t_ellipsis")

        if empresa_tag:
            empresa = empresa_tag.get_text(strip=True)

        # ------------------------
        # Ciudad
        # ------------------------

        ciudad = None

        ciudad_tag = oferta.find("span", class_="mr10")

        if ciudad_tag:
            ciudad = ciudad_tag.get_text(strip=True)

        # ------------------------
        # Fecha
        # ------------------------

        fecha = None

        fecha_tag = oferta.find("p", class_="fs13 fc_aux mt15")

        if fecha_tag:
            fecha = fecha_tag.get_text(strip=True)

        # ------------------------
        # Salario
        # ------------------------

        salario = None

        icono_salario = oferta.find("span", class_="icon i_salary")

        if icono_salario:

            contenedor = icono_salario.parent

            salario = contenedor.get_text(" ", strip=True)

        # ------------------------
        # Link
        # ------------------------

        link = None

        if titulo_tag:

            href = titulo_tag.get("href")

            if href:
                link = "https://ec.computrabajo.com" + href

        datos.append({

            "titulo": titulo,
            "empresa": empresa,
            "ciudad": ciudad,
            "salario": salario,
            "fecha": fecha,
            "link": link

        })

    return datos

# ============================================================
# MAIN
# ============================================================

def main():

    try:

        print("Descargando página...")

        html = obtener_html()

        print("Extrayendo ofertas...")

        datos = extraer_ofertas(html)

        archivo = guardar_json(
            datos,
            "data/raw/scraping/computrabajo_ec",
            "computrabajo"
        )

        print(f"Ofertas encontradas: {len(datos)}")
        print(f"Archivo generado: {archivo}")

    except Exception as e:

        print("Error:", e)

    finally:

        time.sleep(DELAY)


if __name__ == "__main__":

    main()