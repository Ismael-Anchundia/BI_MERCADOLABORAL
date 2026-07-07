"""
==========================================================
STACK OVERFLOW LOADER
==========================================================

Descripción:
Este script carga el dataset Stack Overflow Developer Survey almacenado en la zona Raw.

Su función es verificar que el archivo exista, validar que contenga las columnas mínimas requeridas para el
proyecto y mostrar información general del dataset antes de ser utilizado dentro del pipeline ETL.

Entradas:
- survey_results_public.csv

Salidas:
- Información del dataset en consola.
- Validación del esquema de columnas.
==========================================================
"""

import os
import pandas as pd

# Ruta donde se encuentra el dataset descargado
ARCHIVO = "data/raw/archivos/stackoverflow/survey_results_public.csv"


def validar_columnas(df):
    """
    Verifica que el dataset contenga las columnas
    mínimas necesarias para el proyecto.
    """
    columnas_obligatorias = [
        "Country",
        "Employment",
        "DevType",
        "LanguageHaveWorkedWith"
    ]

    faltantes = []

    for columna in columnas_obligatorias:
        if columna not in df.columns:
            faltantes.append(columna)

    return faltantes

def main():
    """
    Punto principal del programa.

    Lee el archivo CSV, muestra información general, calcula el uso de memoria y valida el esquema
    del dataset.
    """

    print("=" * 50)
    print("STACK OVERFLOW DEVELOPER SURVEY")
    print("=" * 50)

    print("Leyendo dataset...\n")

    df = pd.read_csv(
        ARCHIVO,
        low_memory=False
    )

    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")

    print()

    memoria = df.memory_usage(deep=True).sum() / 1024 / 1024
    print(f"Memoria utilizada: {memoria:.2f} MB")

    print()

    faltantes = validar_columnas(df)

    if len(faltantes) == 0:
        print("Esquema válido")
    else:
        print("Faltan columnas:")

        for c in faltantes:
            print("-", c)

    print()

    print("Primeras columnas del dataset:")

    for columna in df.columns[:15]:
        print("-", columna)


if __name__ == "__main__":
    main()