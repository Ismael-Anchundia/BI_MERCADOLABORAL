import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_fechas.csv"
OUTPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_salarios.csv"


def limpiar_texto(valor):
    if pd.isna(valor):
        return None

    texto = str(valor).strip()
    texto = " ".join(texto.split())

    if texto == "" or texto.lower() in ["nan", "none", "null"]:
        return None

    return texto


def convertir_numero_ecuador(numero_texto):
    """
    Convierte formatos como:
    482,00  -> 482.00
    2.000,00 -> 2000.00
    1200 -> 1200.00
    """
    if not numero_texto:
        return None

    numero_texto = numero_texto.strip()

    if "," in numero_texto:
        numero_texto = numero_texto.replace(".", "")
        numero_texto = numero_texto.replace(",", ".")
    else:
        numero_texto = numero_texto.replace(",", "")

    try:
        return float(numero_texto)
    except ValueError:
        return None


def extraer_salario(salario_raw):
    texto = limpiar_texto(salario_raw)

    if texto is None:
        return None

    texto_min = texto.lower()

    if "a convenir" in texto_min or "no especificado" in texto_min:
        return None

    numeros = re.findall(r"\d[\d\.,]*", texto)

    if not numeros:
        return None

    valores = []

    for n in numeros:
        valor = convertir_numero_ecuador(n)

        if valor is not None:
            valores.append(valor)

    if not valores:
        return None

    # Si hay rango salarial, se usa el promedio.
    if len(valores) >= 2:
        return round(sum(valores[:2]) / 2, 2)

    return round(valores[0], 2)


def main():
    print("=" * 60)
    print("STAGING - CONVERSIÓN Y LIMPIEZA DE SALARIOS")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    df["salario_usd"] = df["salario_raw"].apply(extraer_salario)

    total = len(df)
    salarios_validos = df["salario_usd"].notna().sum()
    salarios_nulos = total - salarios_validos

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Registros procesados: {total}")
    print(f"Salarios convertidos: {salarios_validos}")
    print(f"Salarios nulos/no especificados: {salarios_nulos}")
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()