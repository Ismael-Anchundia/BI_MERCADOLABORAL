"""
==========================================================
QUALITY CHECKS
==========================================================

Descripción:
Este script implementa el Framework de Calidad de Datos del proyecto.

Su función es evaluar el archivo final generado en la zona Staging y aplicar controles automáticos sobre:
- Duplicados.
- Valores nulos.
- Formatos y casting.
- Estandarización.
- Homologación inter-fuentes.
- Métricas finales de calidad.

Entradas:
- ofertas_staging_final.csv

Salidas:
- reporte_calidad_ofertas.csv
- metricas_calidad_resumen.csv
==========================================================
"""

from pathlib import Path
import pandas as pd

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]

# Archivo final generado por la etapa Staging
INPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_staging_final.csv"

# Carpeta donde se almacenan los reportes de calidad
REPORT_DIR = BASE_DIR / "data" / "quality"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Archivos de salida del Framework de Calidad
OUTPUT_REPORT = REPORT_DIR / "reporte_calidad_ofertas.csv"
OUTPUT_SUMMARY = REPORT_DIR / "metricas_calidad_resumen.csv"

# Campos considerados relevantes para evaluar completitud
CAMPOS_CLAVE = [
    "titulo_oferta",
    "empresa",
    "ciudad",
    "fecha_publicacion",
    "url_oferta",
    "fuente",
    "categoria_rol"
]

# ==========================================================
# CONTROL DE NULOS
# ==========================================================

def calcular_nulos(df):
    """
    Calcula la cantidad y porcentaje de valores nulos para cada campo clave del dataset final.
    También asigna una estrategia de tratamiento según la criticidad del campo evaluado.
    """

    resultados = []

    for campo in CAMPOS_CLAVE:
        if campo in df.columns:
            total = len(df)
            nulos = df[campo].isna().sum()
            porcentaje = round((nulos / total) * 100, 2)

            if campo in ["titulo_oferta", "url_oferta", "fuente"]:
                estrategia = "Campo crítico: eliminar o revisar manualmente si está vacío."
            elif campo == "fecha_publicacion":
                estrategia = "Mantener como pendiente si no se pudo interpretar desde Raw."
            elif campo == "ciudad":
                estrategia = "Inferir posteriormente desde descripción o fuente si aplica."
            elif campo == "empresa":
                estrategia = "Mantener como No especificado si la fuente no lo publica."
            else:
                estrategia = "Mantener categoría calculada o asignar Otros."

            resultados.append({
                "control": "Control de nulos",
                "campo": campo,
                "total_registros": total,
                "registros_afectados": nulos,
                "porcentaje": porcentaje,
                "estrategia": estrategia
            })

    return resultados

# ==========================================================
# CONTROL DE DUPLICADOS
# ==========================================================

def calcular_duplicados(df):
    """
    Identifica registros duplicados usando una clave compuesta por título, empresa, ciudad y fuente.
    Esta combinación permite detectar ofertas repetidas dentro de una misma fuente sin eliminar publicaciones
    similares provenientes de portales diferentes.
    """
    clave = ["titulo_oferta", "empresa", "ciudad", "fuente"]

    duplicados = df.duplicated(subset=clave).sum()
    porcentaje = round((duplicados / len(df)) * 100, 2)

    return [{
        "control": "Duplicados",
        "campo": "titulo_oferta + empresa + ciudad + fuente",
        "total_registros": len(df),
        "registros_afectados": duplicados,
        "porcentaje": porcentaje,
        "estrategia": "Mantener el primer registro detectado y eliminar repeticiones posteriores."
    }]

# ==========================================================
# FORMATOS Y CASTING
# ==========================================================

def calcular_formatos_casting(df):
    """
    Evalúa los campos que fueron transformados durante la etapa Staging, principalmente salarios y fechas.
    Permite medir cuántos salarios fueron convertidos correctamente a valores numéricos y cuántas fechas
    fueron normalizadas al formato YYYY-MM-DD.
    """
    resultados = []

    if "salario_usd" in df.columns:
        salarios_validos = df["salario_usd"].notna().sum()
        salarios_nulos = df["salario_usd"].isna().sum()

        resultados.append({
            "control": "Formatos y casting",
            "campo": "salario_usd",
            "total_registros": len(df),
            "registros_afectados": salarios_validos,
            "porcentaje": round((salarios_validos / len(df)) * 100, 2),
            "estrategia": "Conversión de strings salariales a valores numéricos float en USD."
        })

        resultados.append({
            "control": "Salarios no especificados",
            "campo": "salario_usd",
            "total_registros": len(df),
            "registros_afectados": salarios_nulos,
            "porcentaje": round((salarios_nulos / len(df)) * 100, 2),
            "estrategia": "Mantener como nulo cuando la fuente no publica salario."
        })

    if "fecha_publicacion" in df.columns:
        fechas_validas = df["fecha_publicacion"].notna().sum()

        resultados.append({
            "control": "Estandarización de fechas",
            "campo": "fecha_publicacion",
            "total_registros": len(df),
            "registros_afectados": fechas_validas,
            "porcentaje": round((fechas_validas / len(df)) * 100, 2),
            "estrategia": "Conversión a formato ANSI YYYY-MM-DD."
        })

    return resultados

# ==========================================================
# ESTANDARIZACIÓN Y HOMOLOGACIÓN
# ==========================================================

def calcular_estandarizacion(df):
    """
    Evalúa la estandarización de categorías maestras y la integración de datos provenientes de múltiples
    fuentes bajo un esquema común.
    """
    resultados = []

    if "categoria_rol" in df.columns:
        categorias = df["categoria_rol"].nunique()

        resultados.append({
            "control": "Estandarización estricta",
            "campo": "categoria_rol",
            "total_registros": len(df),
            "registros_afectados": categorias,
            "porcentaje": 100,
            "estrategia": "Homogeneización de cargos en categorías maestras."
        })

    if "fuente" in df.columns:
        fuentes = df["fuente"].nunique()

        resultados.append({
            "control": "Homologación inter-fuentes",
            "campo": "fuente",
            "total_registros": len(df),
            "registros_afectados": fuentes,
            "porcentaje": 100,
            "estrategia": "Integración de fuentes heterogéneas bajo un esquema común."
        })

    return resultados

# ==========================================================
# MÉTRICAS FINALES DE CALIDAD
# ==========================================================

def generar_metricas_resumen(df, reporte):
    """
    Genera un resumen ejecutivo con los indicadores principales de calidad del dataset final.
    """
    total = len(df)

    campos_completitud = [
        "titulo_oferta",
        "ciudad",
        "fecha_publicacion",
        "url_oferta",
        "fuente",
        "categoria_rol"
    ]

    total_celdas = total * len(campos_completitud)
    nulos = df[campos_completitud].isna().sum().sum()
    completitud = round(((total_celdas - nulos) / total_celdas) * 100, 2)

    duplicados = df.duplicated(
        subset=["titulo_oferta", "empresa", "ciudad", "fuente"]
    ).sum()

    resumen = pd.DataFrame([
        {
            "metrica_operacional": "Total registros consolidados aptos para Warehouse",
            "valor": total
        },
        {
            "metrica_operacional": "Tasa de completitud general",
            "valor": f"{completitud}%"
        },
        {
            "metrica_operacional": "Registros duplicados remanentes",
            "valor": duplicados
        },
        {
            "metrica_operacional": "Total fuentes integradas",
            "valor": df["fuente"].nunique()
        },
        {
            "metrica_operacional": "Registros con salario normalizado",
            "valor": df["salario_usd"].notna().sum()
        },
        {
            "metrica_operacional": "Registros con fecha normalizada",
            "valor": df["fecha_publicacion"].notna().sum()
        }
    ])

    return resumen

# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():
    """
    Ejecuta todos los controles de calidad y genera los reportes correspondientes en formato CSV.
    """
    print("=" * 70)
    print("FRAMEWORK DE CALIDAD DE DATOS")
    print("=" * 70)

    df = pd.read_csv(INPUT_FILE)

    resultados = []

    resultados.extend(calcular_duplicados(df))
    resultados.extend(calcular_nulos(df))
    resultados.extend(calcular_formatos_casting(df))
    resultados.extend(calcular_estandarizacion(df))

    reporte = pd.DataFrame(resultados)
    resumen = generar_metricas_resumen(df, reporte)

    reporte.to_csv(OUTPUT_REPORT, index=False, encoding="utf-8-sig")
    resumen.to_csv(OUTPUT_SUMMARY, index=False, encoding="utf-8-sig")

    print(f"Registros evaluados: {len(df)}")
    print(f"Controles ejecutados: {reporte['control'].nunique()}")
    print()
    print("Resumen:")
    print(resumen)
    print()
    print(f"Reporte generado: {OUTPUT_REPORT}")
    print(f"Métricas generadas: {OUTPUT_SUMMARY}")

# ==========================================================
# EJECUCIÓN DEL SCRIPT
# ==========================================================

if __name__ == "__main__":
    main()