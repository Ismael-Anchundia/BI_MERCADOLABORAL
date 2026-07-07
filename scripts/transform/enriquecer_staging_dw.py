import re
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_staging_final.csv"
OUTPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_staging_dw.csv"


def limpiar_texto(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def completar_fecha_publicacion(row):
    fecha_publicacion = limpiar_texto(row.get("fecha_publicacion"))
    fecha_raw = limpiar_texto(row.get("fecha_raw"))

    if fecha_publicacion:
        fecha = pd.to_datetime(fecha_publicacion, errors="coerce")
        if not pd.isna(fecha):
            return fecha.strftime("%Y-%m-%d")

    if fecha_raw:
        fecha = pd.to_datetime(fecha_raw, errors="coerce", dayfirst=True)
        if not pd.isna(fecha):
            return fecha.strftime("%Y-%m-%d")

    return None


def extraer_ciudad(valor):
    texto = limpiar_texto(valor)

    if not texto:
        return "No especificado"

    if "," in texto:
        return texto.split(",")[0].strip().title()

    if texto.replace(".", "").replace(",", "").isdigit():
        return "No especificado"

    return texto.strip().title()


def extraer_provincia(valor):
    texto = limpiar_texto(valor)

    if "," in texto:
        return texto.split(",")[1].strip().title()

    return "No especificado"


def inferir_pais(fuente):
    fuente = limpiar_texto(fuente).lower()

    if "_pe" in fuente or "peru" in fuente:
        return "Perú"

    return "Ecuador"


def homologar_modalidad(valor):
    texto = limpiar_texto(valor).lower()

    if "remoto" in texto or "desde casa" in texto or "teletrabajo" in texto:
        return "Remoto"

    if "híbrido" in texto or "hibrido" in texto:
        return "Híbrido"

    if (
        "presencial" in texto
        or "tiempo completo" in texto
        or "medio tiempo" in texto
        or "por contrato" in texto
    ):
        return "Presencial"

    return "No especificado"


def inferir_tipo_fuente(fuente):
    fuente = limpiar_texto(fuente).lower()

    if "api" in fuente:
        return "API"

    return "Scraping"


def detectar_tecnologia(titulo, descripcion):
    texto = f"{limpiar_texto(titulo)} {limpiar_texto(descripcion)}".lower()

    tecnologias = {
        "Python": ["python"],
        "JavaScript": ["javascript", "js", "jquery"],
        "PHP": ["php"],
        "Laravel": ["laravel"],
        "React": ["react"],
        "Vue.js": ["vue"],
        "Angular": ["angular"],
        "Node.js": ["nodejs", "node.js", "node js"],
        "Java": ["java "],
        "C#": ["c#", ".net"],
        "SQL": ["sql", "postgresql", "mysql", "sql server"],
        "Power BI": ["power bi"],
        "Excel": ["excel"],
        "Docker": ["docker"],
        "AWS": ["aws"],
        "Azure": ["azure"],
        "Git": ["git", "github"],
        "API REST": ["api rest", "rest api", "web services", "servicios web"],
    }

    for tecnologia, palabras in tecnologias.items():
        for palabra in palabras:
            if palabra in texto:
                return tecnologia

    return "No especificado"


def categorizar_tecnologia(tecnologia):
    categorias = {
        "Python": "Lenguaje",
        "JavaScript": "Lenguaje",
        "PHP": "Lenguaje",
        "Java": "Lenguaje",
        "C#": "Lenguaje",
        "Laravel": "Framework",
        "React": "Framework",
        "Vue.js": "Framework",
        "Angular": "Framework",
        "Node.js": "Framework",
        "SQL": "Base de Datos",
        "Power BI": "BI",
        "Excel": "Herramienta",
        "Docker": "DevOps",
        "AWS": "Cloud",
        "Azure": "Cloud",
        "Git": "Herramienta",
        "API REST": "Integración",
    }

    return categorias.get(tecnologia, "No especificado")


def extraer_experiencia(titulo, descripcion):
    texto = f"{limpiar_texto(titulo)} {limpiar_texto(descripcion)}".lower()

    patron = r"(\d+)\s*(años|año|anos|ano)"
    coincidencia = re.search(patron, texto)

    if coincidencia:
        return int(coincidencia.group(1))

    return None


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    # Completar fechas faltantes usando fecha_raw
    df["fecha_publicacion"] = df.apply(completar_fecha_publicacion, axis=1)

    df["ciudad_limpia"] = df["ciudad"].apply(extraer_ciudad)
    df["provincia"] = df["ciudad"].apply(extraer_provincia)
    df["pais"] = df["fuente"].apply(inferir_pais)

    df["nombre_rol"] = df["titulo_oferta"].apply(
        lambda x: limpiar_texto(x).title() if limpiar_texto(x) else "No especificado"
    )

    df["modalidad"] = df["modalidad_raw"].apply(homologar_modalidad)

    df["nombre_tecnologia"] = df.apply(
        lambda row: detectar_tecnologia(row.get("titulo_oferta"), row.get("descripcion_raw")),
        axis=1,
    )

    df["categoria_tecnologia"] = df["nombre_tecnologia"].apply(categorizar_tecnologia)

    df["tipo_fuente"] = df["fuente"].apply(inferir_tipo_fuente)

    df["num_vacantes"] = 1

    df["experiencia_anios"] = df.apply(
        lambda row: extraer_experiencia(row.get("titulo_oferta"), row.get("descripcion_raw")),
        axis=1,
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("=" * 70)
    print("STAGING ENRIQUECIDO PARA DATA WAREHOUSE")
    print("=" * 70)
    print(f"Archivo origen: {INPUT_FILE}")
    print(f"Archivo generado: {OUTPUT_FILE}")
    print(f"Registros procesados: {len(df)}")

    fechas_invalidas = pd.to_datetime(df["fecha_publicacion"], errors="coerce").isna().sum()
    print(f"Fechas inválidas pendientes: {fechas_invalidas}")

    print()
    print("Columnas generadas:")
    nuevas_columnas = [
        "ciudad_limpia",
        "provincia",
        "pais",
        "nombre_rol",
        "modalidad",
        "nombre_tecnologia",
        "categoria_tecnologia",
        "tipo_fuente",
        "num_vacantes",
        "experiencia_anios",
    ]

    for columna in nuevas_columnas:
        print(f"- {columna}")

    print()
    print("Vista previa:")
    print(
        df[
            [
                "titulo_oferta",
                "fecha_publicacion",
                "ciudad_limpia",
                "provincia",
                "pais",
                "modalidad",
                "nombre_tecnologia",
                "categoria_tecnologia",
                "categoria_rol",
                "salario_usd",
                "num_vacantes",
                "experiencia_anios",
            ]
        ].head(10)
    )

    print()
    print("Registros con fecha inválida:")
    fechas = pd.to_datetime(df["fecha_publicacion"], errors="coerce")
    print(
        df[fechas.isna()][
            [
                "titulo_oferta",
                "empresa",
                "fecha_raw",
                "fecha_publicacion",
                "fuente",
            ]
        ]
    )


if __name__ == "__main__":
    main()