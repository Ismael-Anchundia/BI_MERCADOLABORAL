"""
==========================================================
GITHUB API
==========================================================

Descripción:
Este script consume la API pública de GitHub para obtener información de los repositorios más populares
relacionados con el término "software".

La información obtenida se almacena directamente en la zona Raw del proyecto sin realizar modificaciones,
preservando la integridad de los datos originales.

Entradas:
- GitHub REST API

Salidas:
- github_YYYY-MM-DD.json almacenado en:
  data/raw/api/github/
==========================================================
"""

import os
import sys
import time
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import HEADERS, TIMEOUT, DELAY
from utils.helpers import guardar_json

# ============================================================
# CONFIGURACIÓN
# ============================================================

URL = "https://api.github.com/search/repositories"

PARAMS = {
    "q": "software",
    "sort": "stars",
    "order": "desc",
    "per_page": 20
}

# ============================================================
# OBTENER DATOS
# ============================================================

def obtener_repositorios():
    """
    Realiza la petición HTTP GET hacia la API de GitHub utilizando los parámetros configurados.
    Retorna el contenido de la respuesta en formato JSON.
    """

    respuesta = requests.get(
        URL,
        headers=HEADERS,
        params=PARAMS,
        timeout=TIMEOUT
    )

    respuesta.raise_for_status()

    return respuesta.json()

# ============================================================
# EXTRAER INFORMACIÓN
# ============================================================

def procesar_repositorios(datos_api):
    """
    Extrae únicamente los atributos de interés de cada repositorio para el análisis de tendencias
    tecnológicas.
    """

    repositorios = []

    for repo in datos_api["items"]:

        repositorios.append({

            "nombre": repo["name"],

            "propietario": repo["owner"]["login"],

            "lenguaje": repo["language"],

            "estrellas": repo["stargazers_count"],

            "forks": repo["forks_count"],

            "creado": repo["created_at"],

            "actualizado": repo["updated_at"],

            "url": repo["html_url"]

        })

    return repositorios

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    """
    Ejecuta el proceso completo de extracción desde la API de GitHub y almacena el resultado en la zona Raw.
    """

    try:

        print("Consultando GitHub API...")

        datos = obtener_repositorios()

        repos = procesar_repositorios(datos)

        archivo = guardar_json(
            repos,
            "data/raw/api/github",
            "github"
        )

        print(f"Repositorios encontrados: {len(repos)}")
        print(f"Archivo generado: {archivo}")

    except Exception as e:

        print("Error:", e)

    finally:

        time.sleep(DELAY)

if __name__ == "__main__":
    main()