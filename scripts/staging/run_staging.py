"""
==========================================================
RUN STAGING
==========================================================

Descripción:
Este script automatiza la ejecución completa de la etapa de Staging del pipeline ETL.

Su función es ejecutar, en el orden correcto, todos los procesos de transformación necesarios para convertir los
datos almacenados en la zona Raw en un conjunto de datos integrado, limpio y listo para la etapa de calidad.

Procesos ejecutados:
1. Homologación de columnas.
2. Estandarización de fechas.
3. Conversión de salarios.
4. Clasificación de roles.
5. Eliminación de registros duplicados.

Salida:
- ofertas_staging_final.csv
==========================================================
"""

import subprocess
import sys
from pathlib import Path

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]

# Lista de scripts que conforman el proceso de Staging.
# Se ejecutan en el orden definido para garantizar la correcta transformación de los datos.
SCRIPTS = [
    "stg_normalize_columns.py",
    "stg_dates.py",
    "stg_currency.py",
    "stg_roles.py",
    "stg_dedup.py"
]


def ejecutar_script(script):
    """
    Ejecuta un script de la carpeta staging.
    Si alguno de los procesos falla, se detiene la ejecución completa del pipeline para evitar generar
    datos inconsistentes.
    """

    ruta_script = BASE_DIR / "scripts" / "staging" / script

    print("\n" + "=" * 70)
    print(f"Ejecutando: {script}")
    print("=" * 70)

    resultado = subprocess.run(
        [sys.executable, str(ruta_script)],
        cwd=BASE_DIR
    )

    if resultado.returncode != 0:
        raise RuntimeError(f"Error ejecutando {script}")

# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():
    """
    Ejecuta de forma secuencial todos los procesos de
    transformación correspondientes a la etapa Staging.
    """

    print("=" * 70)
    print("PIPELINE STAGING - RAW → STAGING")
    print("=" * 70)

    for script in SCRIPTS:
        ejecutar_script(script)

    print("\n" + "=" * 70)
    print("PIPELINE STAGING FINALIZADO CORRECTAMENTE")
    print("=" * 70)
    print("Archivo final generado:")
    print(BASE_DIR / "data" / "staging" / "ofertas_staging_final.csv")


# ==========================================================
# EJECUCIÓN DEL SCRIPT
# ==========================================================
if __name__ == "__main__":
    main()