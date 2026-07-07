import os
import sys
import time
import re
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import HEADERS, TIMEOUT, DELAY
from utils.helpers import guardar_json


BASE_URL = "https://ec.trabajosdiarios.com"

SEARCH_URLS = [
    "https://ec.trabajosdiarios.com/ofertas-trabajo/de-software",
    "https://ec.trabajosdiarios.com/ofertas-trabajo/de-desarrollador",
    "https://ec.trabajosdiarios.com/ofertas-trabajo/de-programador",
    "https://ec.trabajosdiarios.com/ofertas-trabajo/de-java"
]

MAX_PAGES = 3


def obtener_html(url):
    respuesta = requests.get(
        url,
        headers=HEADERS,
        timeout=TIMEOUT
    )
    respuesta.raise_for_status()
    return respuesta.text


def limpiar_texto(texto):
    if not texto:
        return None
    return " ".join(texto.split())


def extraer_fecha(texto):
    patron = r"\d{2}/\d{2}/\d{4}"
    coincidencia = re.search(patron, texto)
    return coincidencia.group(0) if coincidencia else None


def extraer_salario(texto):
    patron = r"\$\s?[\d\.,]+"
    coincidencia = re.search(patron, texto)
    return coincidencia.group(0) if coincidencia else None


def extraer_modalidad(texto):
    modalidades = {
        "Tiempo Completo": "Tiempo Completo",
        "Medio Tiempo": "Medio Tiempo",
        "Por Contrato": "Por Contrato",
        "Desde Casa": "Desde Casa",
        "Prácticas / Becario": "Prácticas",
        "Prácticas": "Prácticas",
        "Por Horas / Freelance": "Freelance",
        "Freelance": "Freelance"
    }

    for clave, valor in modalidades.items():
        if clave.lower() in texto.lower():
            return valor

    return None


def extraer_ciudad(texto):
    patron = r"(Quito|Guayaquil|Cuenca|Durán|Duran|Chongon|Chongón|Teletrabajo|Ecuador|Pichincha|Guayas|Azuay|Esmeraldas|Manabí|Napo|Orellana|Morona Santiago|Bolívar)"
    coincidencia = re.search(patron, texto, re.IGNORECASE)

    if coincidencia:
        return coincidencia.group(0)

    return None


def limpiar_titulo(titulo):
    if not titulo:
        return None

    titulo = titulo.replace("Premium", "").strip()
    return limpiar_texto(titulo)


def extraer_ofertas(html, url_origen):
    soup = BeautifulSoup(html, "html.parser")

    ofertas = []
    vistos = set()

    enlaces = soup.find_all("a", href=True)

    for enlace in enlaces:
        href = enlace.get("href", "")

        if not href.startswith("/trabajo/"):
            continue

        link = BASE_URL + href

        if link in vistos:
            continue

        vistos.add(link)

        texto_oferta = limpiar_texto(enlace.get_text(" ", strip=True))

        if not texto_oferta or len(texto_oferta) < 40:
            continue

        fecha = extraer_fecha(texto_oferta)
        salario = extraer_salario(texto_oferta)
        modalidad = extraer_modalidad(texto_oferta)
        ciudad = extraer_ciudad(texto_oferta)

        titulo = limpiar_titulo(texto_oferta)

        ofertas.append({
            "titulo": titulo,
            "empresa": None,
            "ciudad": ciudad,
            "modalidad": modalidad,
            "salario": salario,
            "fecha": fecha,
            "descripcion_raw": texto_oferta,
            "link": link,
            "url_origen": url_origen
        })

    return ofertas


def construir_url(base, pagina):
    if pagina == 1:
        return base
    return f"{base}?page={pagina}"


def main():
    datos_totales = []

    try:
        for search_url in SEARCH_URLS:
            for pagina in range(1, MAX_PAGES + 1):
                url = construir_url(search_url, pagina)

                print(f"Descargando: {url}")

                try:
                    html = obtener_html(url)
                    datos = extraer_ofertas(html, url)

                    print(f"Ofertas detectadas: {len(datos)}")

                    datos_totales.extend(datos)

                    time.sleep(DELAY)

                except requests.exceptions.HTTPError as e:
                    print(f"Error HTTP en {url}: {e}")

                except requests.exceptions.Timeout:
                    print(f"Timeout en {url}")

                except Exception as e:
                    print(f"Error general en {url}: {e}")

        # Deduplicación final por link
        unicos = {}
        for oferta in datos_totales:
            unicos[oferta["link"]] = oferta

        datos_totales = list(unicos.values())

        archivo = guardar_json(
            datos_totales,
            "data/raw/scraping/trabajosdiarios",
            "trabajosdiarios"
        )

        print(f"Total ofertas únicas guardadas: {len(datos_totales)}")
        print(f"Archivo generado: {archivo}")

    except Exception as e:
        print("Error general:", e)


if __name__ == "__main__":
    main()