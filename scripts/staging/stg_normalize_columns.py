import json
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw" / "scraping"
STAGING_DIR = BASE_DIR / "data" / "staging"

STAGING_DIR.mkdir(parents=True, exist_ok=True)


def leer_json_mas_reciente(carpeta_fuente):
    archivos = list(carpeta_fuente.glob("*.json"))

    if not archivos:
        return []

    archivo_reciente = max(archivos, key=lambda x: x.stat().st_mtime)

    with open(archivo_reciente, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return datos


def normalizar_computrabajo(registros, fuente):
    filas = []

    for r in registros:
        filas.append({
            "titulo_oferta": r.get("titulo"),
            "empresa": r.get("empresa"),
            "ciudad": r.get("ciudad"),
            "salario_raw": r.get("salario"),
            "fecha_raw": r.get("fecha"),
            "modalidad_raw": None,
            "descripcion_raw": None,
            "url_oferta": r.get("link"),
            "fuente": fuente
        })

    return filas


def normalizar_trabajosdiarios(registros):
    filas = []

    for r in registros:
        filas.append({
            "titulo_oferta": r.get("titulo"),
            "empresa": r.get("empresa"),
            "ciudad": r.get("ciudad"),
            "salario_raw": r.get("salario"),
            "fecha_raw": r.get("fecha"),
            "modalidad_raw": r.get("modalidad"),
            "descripcion_raw": r.get("descripcion_raw"),
            "url_oferta": r.get("link"),
            "fuente": "trabajosdiarios"
        })

    return filas


def normalizar_unmejorempleo(registros):
    filas = []

    for r in registros:
        filas.append({
            "titulo_oferta": r.get("titulo"),
            "empresa": r.get("empresa"),
            "ciudad": r.get("ciudad"),
            "salario_raw": r.get("salario"),
            "fecha_raw": r.get("fecha"),
            "modalidad_raw": r.get("modalidad"),
            "descripcion_raw": r.get("descripcion_raw"),
            "url_oferta": r.get("link"),
            "fuente": "unmejorempleo"
        })

    return filas


def normalizar_multitrabajos(registros):
    filas = []

    for r in registros:
        filas.append({
            "titulo_oferta": r.get("titulo"),
            "empresa": r.get("empresa"),
            "ciudad": r.get("localizacion"),
            "salario_raw": None,
            "fecha_raw": r.get("fechaPublicacion"),
            "modalidad_raw": r.get("modalidadTrabajo"),
            "descripcion_raw": r.get("detalle"),
            "url_oferta": r.get("link"),
            "fuente": "multitrabajos"
        })

    return filas


def main():
    print("=" * 60)
    print("STAGING - HOMOLOGACIÓN DE NOMBRES")
    print("=" * 60)

    filas_totales = []

    fuentes = {
        "computrabajo_ec": lambda datos: normalizar_computrabajo(datos, "computrabajo_ec"),
        "computrabajo_pe": lambda datos: normalizar_computrabajo(datos, "computrabajo_pe"),
        "trabajosdiarios": normalizar_trabajosdiarios,
        "unmejorempleo": normalizar_unmejorempleo,
        "multitrabajos": normalizar_multitrabajos
    }

    for nombre_fuente, funcion_normalizar in fuentes.items():
        carpeta = RAW_DIR / nombre_fuente

        if not carpeta.exists():
            print(f"⚠️ Carpeta no encontrada: {carpeta}")
            continue

        registros = leer_json_mas_reciente(carpeta)

        print(f"Fuente: {nombre_fuente} | Registros Raw: {len(registros)}")

        filas_normalizadas = funcion_normalizar(registros)

        print(f"Registros normalizados: {len(filas_normalizadas)}")

        filas_totales.extend(filas_normalizadas)

    df = pd.DataFrame(filas_totales)

    salida = STAGING_DIR / "ofertas_normalizadas.csv"

    df.to_csv(salida, index=False, encoding="utf-8-sig")

    print()
    print(f"Total registros integrados: {len(df)}")
    print(f"Archivo generado: {salida}")


if __name__ == "__main__":
    main()