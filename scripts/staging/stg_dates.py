import re
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_normalizadas.csv"
OUTPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_fechas.csv"

FECHA_EXTRACCION = datetime.today()

MESES = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "setiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12
}


def limpiar_texto(valor):
    if pd.isna(valor):
        return None

    texto = str(valor).strip()
    texto = " ".join(texto.split())

    if texto == "" or texto.lower() in ["nan", "none", "null"]:
        return None

    return texto


def normalizar_fecha(fecha_raw):
    texto = limpiar_texto(fecha_raw)

    if texto is None:
        return None

    texto_min = texto.lower()

    # Formato ISO: 2026-07-01T15:22:00Z
    try:
        if re.match(r"^\d{4}-\d{2}-\d{2}", texto):
            return pd.to_datetime(texto, errors="coerce").strftime("%Y-%m-%d")
    except Exception:
        pass

    # Formato dd/mm/yyyy
    match = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", texto)
    if match:
        dia = int(match.group(1))
        mes = int(match.group(2))
        anio = int(match.group(3))

        try:
            return datetime(anio, mes, dia).strftime("%Y-%m-%d")
        except ValueError:
            return None

    # Ejemplo: 18 de junio
    match = re.search(r"(\d{1,2})\s+de\s+([a-záéíóúñ]+)", texto_min)
    if match:
        dia = int(match.group(1))
        mes_nombre = match.group(2)

        mes = MESES.get(mes_nombre)

        if mes:
            anio = FECHA_EXTRACCION.year

            try:
                fecha = datetime(anio, mes, dia)

                # Si la fecha calculada queda en el futuro,
                # se asume que corresponde al año anterior.
                if fecha > FECHA_EXTRACCION:
                    fecha = datetime(anio - 1, mes, dia)

                return fecha.strftime("%Y-%m-%d")

            except ValueError:
                return None

    # Ejemplo: Hace 3 días
    match = re.search(r"hace\s+(\d+)\s+d[ií]as", texto_min)
    if match:
        dias = int(match.group(1))
        return (FECHA_EXTRACCION - timedelta(days=dias)).strftime("%Y-%m-%d")

    # Ejemplo: Hace 6 horas
    match = re.search(r"hace\s+(\d+)\s+horas", texto_min)
    if match:
        return FECHA_EXTRACCION.strftime("%Y-%m-%d")

    # Ayer
    if "ayer" in texto_min:
        return (FECHA_EXTRACCION - timedelta(days=1)).strftime("%Y-%m-%d")

    # Más de 30 días
    if "más de 30" in texto_min or "mas de 30" in texto_min:
        return (FECHA_EXTRACCION - timedelta(days=30)).strftime("%Y-%m-%d")

    return None


def main():
    print("=" * 60)
    print("STAGING - ESTANDARIZACIÓN DE FECHAS")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    df["fecha_publicacion"] = df["fecha_raw"].apply(normalizar_fecha)

    total = len(df)
    fechas_validas = df["fecha_publicacion"].notna().sum()
    fechas_invalidas = total - fechas_validas

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Registros procesados: {total}")
    print(f"Fechas normalizadas: {fechas_validas}")
    print(f"Fechas no interpretadas: {fechas_invalidas}")
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()