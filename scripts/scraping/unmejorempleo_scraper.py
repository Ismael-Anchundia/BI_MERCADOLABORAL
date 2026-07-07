import os
import sys
import time
import re
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import HEADERS, TIMEOUT, DELAY
from utils.helpers import guardar_json


BASE_URL = "https://www.unmejorempleo.com.ec"

URLS_OFERTAS = [
    "https://www.unmejorempleo.com.ec/empleo-en_guayas_desarrolladores_de_software-4490591.html",
    "https://www.unmejorempleo.com.ec/empleo-en_guayas_desarrollador_de_software-5367479.html",
    "https://www.unmejorempleo.com.ec/empleo-en_guayas_desarrollador_php_-_remoto-5506735.html",
    "https://www.unmejorempleo.com.ec/empleo-en_guayas_desarrollador_de_software_guayaquil-5237332.html",
    "https://www.unmejorempleo.com.ec/empleo-en_guayas_desarrollador_de_software-4695637.html",
    "https://www.unmejorempleo.com.ec/empleo-en_guayas_ing_de_procesos_software-5442700.html",
    "https://www.unmejorempleo.com.ec/empleo-en_guayas_mantenimiento_de_software_y_hareware-5725494.html"
]


def limpiar_texto(texto):
    if not texto:
        return None
    return " ".join(texto.split())


def obtener_html(url):
    respuesta = requests.get(
        url,
        headers=HEADERS,
        timeout=TIMEOUT
    )
    respuesta.raise_for_status()
    return respuesta.text


def extraer_campo(texto, etiqueta):
    patron = rf"{etiqueta}\s*:?\s*(.*?)(?=Ubicación|Provincia|Salario|Tipo de Contratación|Descripción de la Plaza|Mínimo Nivel|Fecha|$)"
    coincidencia = re.search(patron, texto, re.IGNORECASE)

    if coincidencia:
        return limpiar_texto(coincidencia.group(1))

    return None


def extraer_fecha(texto):
    patrones = [
        r"Publicación:\s*([0-9]{2}/[0-9]{2}/[0-9]{4})",
        r"Fecha:\s*([0-9]{2}/[0-9]{2}/[0-9]{4})",
        r"actualizado\s+el\s+([0-9]{2}\s+\w+\s+[0-9]{4})",
        r"actualizado\s+hace\s+más\s+de\s+[0-9]+\s+días"
    ]

    for patron in patrones:
        coincidencia = re.search(patron, texto, re.IGNORECASE)
        if coincidencia:
            return limpiar_texto(coincidencia.group(1) if coincidencia.groups() else coincidencia.group(0))

    return None


def extraer_salario(texto):
    patrones = [
        r"Salario:\s*(.*?)(?=Tipo de Contratación|Descripción de la Plaza|Mínimo Nivel|$)",
        r"\$\s?[\d\.,]+"
    ]

    for patron in patrones:
        coincidencia = re.search(patron, texto, re.IGNORECASE)
        if coincidencia:
            return limpiar_texto(coincidencia.group(1) if coincidencia.groups() else coincidencia.group(0))

    return None


def extraer_modalidad(texto):
    texto_min = texto.lower()

    if "teletrabajo" in texto_min or "remoto" in texto_min:
        return "Remoto"
    if "híbrido" in texto_min or "hibrido" in texto_min:
        return "Híbrido"
    if "tiempo completo" in texto_min:
        return "Tiempo Completo"
    if "medio tiempo" in texto_min:
        return "Medio Tiempo"
    if "por contrato" in texto_min:
        return "Por Contrato"

    return None


def extraer_ciudad(texto):
    ciudades = [
        "Guayaquil", "Quito", "Cuenca", "Samborondon", "Samborondón",
        "Durán", "Duran", "Manta", "Loja", "Machala", "Ambato",
        "Urdesa", "Guayas", "Pichincha", "Azuay", "Manabí", "El Oro"
    ]

    for ciudad in ciudades:
        if ciudad.lower() in texto.lower():
            return ciudad

    return None


def extraer_titulo(soup, texto):
    h1 = soup.find("h1")
    if h1:
        return limpiar_texto(h1.get_text(" ", strip=True))

    title = soup.find("title")
    if title:
        titulo = limpiar_texto(title.get_text(" ", strip=True))
        if titulo:
            return titulo.replace(" - Un Mejor Empleo", "")

    primera_linea = texto.split("Descripción de la Plaza")[0]
    return limpiar_texto(primera_linea[:120])


def extraer_descripcion(texto):
    patron = r"Descripción de la Plaza(.*?)(?=Mínimo Nivel Académico Requerido|EMPLEOS RELACIONADOS|$)"
    coincidencia = re.search(patron, texto, re.IGNORECASE)

    if coincidencia:
        return limpiar_texto(coincidencia.group(1))

    return texto


def extraer_oferta(url):
    html = obtener_html(url)
    soup = BeautifulSoup(html, "html.parser")

    texto = limpiar_texto(soup.get_text(" ", strip=True))

    titulo = extraer_titulo(soup, texto)
    descripcion = extraer_descripcion(texto)

    oferta = {
        "titulo": titulo,
        "empresa": None,
        "ciudad": extraer_ciudad(texto),
        "modalidad": extraer_modalidad(texto),
        "salario": extraer_salario(texto),
        "fecha": extraer_fecha(texto),
        "descripcion_raw": descripcion,
        "link": url,
        "url_origen": url
    }

    return oferta


def main():
    datos = []

    for url in URLS_OFERTAS:
        print(f"Descargando: {url}")

        try:
            oferta = extraer_oferta(url)
            datos.append(oferta)
            print(f"Oferta extraída: {oferta.get('titulo')}")

            time.sleep(DELAY)

        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP en {url}: {e}")

        except requests.exceptions.Timeout:
            print(f"Timeout en {url}")

        except Exception as e:
            print(f"Error general en {url}: {e}")

    archivo = guardar_json(
        datos,
        "data/raw/scraping/unmejorempleo",
        "unmejorempleo"
    )

    print(f"Total ofertas guardadas: {len(datos)}")
    print(f"Archivo generado: {archivo}")


if __name__ == "__main__":
    main()