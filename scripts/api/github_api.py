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
# MAIN
# ============================================================

def main():

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