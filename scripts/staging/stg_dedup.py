from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_roles.csv"
OUTPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_staging_final.csv"


def limpiar_clave(valor):
    if pd.isna(valor):
        return ""

    return str(valor).lower().strip()


def main():
    print("=" * 60)
    print("STAGING - DEDUPLICACIÓN INTEGRAL")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    total_inicial = len(df)

    df["clave_deduplicacion"] = (
        df["titulo_oferta"].apply(limpiar_clave) + "|" +
        df["empresa"].apply(limpiar_clave) + "|" +
        df["ciudad"].apply(limpiar_clave) + "|" +
        df["fuente"].apply(limpiar_clave)
    )

    duplicados = df.duplicated(subset=["clave_deduplicacion"]).sum()

    df_final = df.drop_duplicates(
        subset=["clave_deduplicacion"],
        keep="first"
    )

    total_final = len(df_final)

    df_final.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Registros iniciales: {total_inicial}")
    print(f"Duplicados detectados: {duplicados}")
    print(f"Registros finales: {total_final}")
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()