"""
==========================================================
ENCUESTA LOADER
==========================================================

Descripción:
Este script carga la encuesta elaborada por el equipo mediante Google Forms, la cual constituye la fuente
propia de información del proyecto.

Su función es validar que el archivo exista, comprobar que contiene todas las columnas requeridas y mostrar
información general sobre los registros recolectados.

Entradas:
- Encuesta_Mercado_Laboral_TI_Ecuador.csv

Salidas:
- Validación del esquema.
- Información estadística básica.
- Visualización de los primeros registros.
==========================================================
"""

from pathlib import Path
import pandas as pd


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]

# Ruta del archivo CSV exportado desde Google Forms
ARCHIVO = BASE_DIR / "data" / "raw" / "fuente_propia" / "Encuesta_Mercado_Laboral_TI_Ecuador.csv"


# ==========================================================
# VALIDACIÓN DE COLUMNAS
# ==========================================================

def validar_columnas(df):
    """
    Verifica que la encuesta contenga todas las columnas definidas durante el diseño del instrumento de
    recolección de datos.
    """

    columnas_obligatorias = [
        "Marca temporal",
        "1. ¿En qué provincia del Ecuador reside actualmente?",
        "2. ¿Actualmente trabaja en el área de desarrollo de software o tecnologías de la información?",
        "3. ¿Cuál es su modalidad laboral preferida?",
        "4. ¿Cuál es su cargo o perfil profesional actual?",
        "5. ¿Cuál es el principal lenguaje de programación que utiliza?",
        "6. ¿Cuántos años de experiencia posee en el área tecnológica?",
        "7. ¿Cuál es el rango aproximado de su ingreso mensual?",
        "8. ¿Qué tecnología utiliza con mayor frecuencia?",
        "9. ¿Qué factor considera más importante al momento de aceptar una oferta laboral?",
        "10. ¿Tiene interés en cambiar de empleo durante los próximos 12 meses?"
    ]

    faltantes = []

    for columna in columnas_obligatorias:

        if columna not in df.columns:
            faltantes.append(columna)

    return faltantes


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():
    """
    Lee el archivo CSV generado por Google Forms, elimina espacios innecesarios en los encabezados,
    valida el esquema y muestra información general de la encuesta.
    """

    print("=" * 55)
    print("FUENTE PROPIA - ENCUESTA MERCADO LABORAL TI")
    print("=" * 55)

    print("Leyendo encuesta...\n")

    df = pd.read_csv(ARCHIVO)

    # Elimina espacios en blanco al inicio y al final
    df.columns = df.columns.str.strip()

    print(f"Registros : {df.shape[0]}")
    print(f"Columnas  : {df.shape[1]}")

    print()

    memoria = df.memory_usage(deep=True).sum() / 1024 / 1024

    print(f"Memoria utilizada: {memoria:.2f} MB")

    print()

    faltantes = validar_columnas(df)

    if len(faltantes) == 0:

        print("Esquema válido")

    else:

        print("Faltan columnas:")

        for columna in faltantes:
            print("-", columna)

    print()

    print("Columnas detectadas:")

    for columna in df.columns:
        print("-", columna)

    print()

    print("Primeros registros:")

    print(df.head())


# ==========================================================
# EJECUCIÓN
# ==========================================================

if __name__ == "__main__":
    main()