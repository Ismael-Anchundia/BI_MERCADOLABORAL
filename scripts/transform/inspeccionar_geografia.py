import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_staging_final.csv"


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    columnas_requeridas = ["ciudad", "fuente", "titulo_oferta", "descripcion_raw"]

    faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            f"Faltan columnas requeridas en el CSV: {faltantes}"
        )

    print("=" * 80)
    print("INSPECCIÓN DE DATOS GEOGRÁFICOS")
    print("=" * 80)

    print(f"Registros totales: {len(df)}")
    print()

    print("VALORES ÚNICOS DE LA COLUMNA CIUDAD")
    print("-" * 80)

    valores_ciudad = (
        df["ciudad"]
        .fillna("VACÍO")
        .astype(str)
        .str.strip()
        .value_counts(dropna=False)
    )

    print(valores_ciudad.to_string())

    print()
    print("=" * 80)
    print("REGISTROS CON CIUDAD POSIBLEMENTE INVÁLIDA")
    print("=" * 80)

    ciudad_texto = (
        df["ciudad"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    mascara_invalida = (
        ciudad_texto.eq("")
        | ciudad_texto.str.fullmatch(r"\d+[.,]\d+|\d+", na=False)
        | ciudad_texto.str.lower().isin(
            [
                "ecuador",
                "perú",
                "peru",
                "teletrabajo",
                "remoto",
                "guayas",
                "pichincha",
                "bolívar",
                "bolivar",
            ]
        )
    )

    columnas_salida = [
        "titulo_oferta",
        "ciudad",
        "fuente",
        "fecha_publicacion",
    ]

    print(
        df.loc[mascara_invalida, columnas_salida]
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()