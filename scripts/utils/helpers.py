import json
import os
from datetime import datetime


def guardar_json(datos, carpeta_destino, nombre_archivo):
    """
    Guarda una lista de diccionarios como JSON.
    """

    fecha = datetime.now().strftime("%Y-%m-%d")

    os.makedirs(carpeta_destino, exist_ok=True)

    ruta = os.path.join(
        carpeta_destino,
        f"{nombre_archivo}_{fecha}.json"
    )

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    return ruta