from pathlib import Path
from datetime import datetime
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_staging_final.csv"
LOG_DIR = BASE_DIR / "data" / "quality"
LOG_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_LOG = LOG_DIR / "error_log_calidad.csv"


def registrar_error(logs, fuente, tipo_error, descripcion, accion):
    logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fuente": fuente,
        "tipo_error": tipo_error,
        "descripcion": descripcion,
        "accion_tomada": accion
    })


def main():
    print("=" * 70)
    print("REGISTRO DE ERRORES - CALIDAD DE DATOS")
    print("=" * 70)

    df = pd.read_csv(INPUT_FILE)
    logs = []

    campos_criticos = ["titulo_oferta", "url_oferta", "fuente"]

    for campo in campos_criticos:
        nulos = df[df[campo].isna()]

        for fuente, grupo in nulos.groupby("fuente"):
            registrar_error(
                logs,
                fuente,
                "Nulo crítico",
                f"Campo {campo} nulo en {len(grupo)} registros.",
                "Registros marcados para revisión o eliminación antes del DW."
            )

    if "fecha_publicacion" in df.columns:
        fechas_nulas = df[df["fecha_publicacion"].isna()]

        for fuente, grupo in fechas_nulas.groupby("fuente"):
            registrar_error(
                logs,
                fuente,
                "Fecha no interpretada",
                f"Fecha no normalizada en {len(grupo)} registros.",
                "Se mantiene como pendiente por falta de patrón reconocible."
            )

    if "salario_usd" in df.columns:
        salarios_nulos = df[df["salario_usd"].isna()]

        for fuente, grupo in salarios_nulos.groupby("fuente"):
            registrar_error(
                logs,
                fuente,
                "Salario no publicado",
                f"Salario no disponible en {len(grupo)} registros.",
                "Se mantiene nulo porque la fuente no publica el dato."
            )

    log_df = pd.DataFrame(logs)

    log_df.to_csv(OUTPUT_LOG, index=False, encoding="utf-8-sig")

    print(f"Eventos registrados: {len(log_df)}")
    print(f"Archivo generado: {OUTPUT_LOG}")


if __name__ == "__main__":
    main()