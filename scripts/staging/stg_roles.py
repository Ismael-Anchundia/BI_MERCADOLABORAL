from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_salarios.csv"
OUTPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_roles.csv"


def limpiar_texto(valor):
    if pd.isna(valor):
        return ""

    return str(valor).lower().strip()


def clasificar_rol(titulo, descripcion):
    texto = f"{limpiar_texto(titulo)} {limpiar_texto(descripcion)}"

    if any(p in texto for p in ["frontend", "front-end", "react", "angular", "vue"]):
        return "Frontend"

    if any(p in texto for p in ["backend", "back-end", "api", "laravel", "django", "spring", "node"]):
        return "Backend"

    if any(p in texto for p in ["full stack", "fullstack", "full-stack"]):
        return "Full Stack"

    if any(p in texto for p in ["data", "datos", "bi", "business intelligence", "analista de datos"]):
        return "Data / BI"

    if any(p in texto for p in ["qa", "tester", "testing", "calidad"]):
        return "QA / Testing"

    if any(p in texto for p in ["devops", "docker", "kubernetes", "cloud", "aws", "azure"]):
        return "DevOps / Cloud"

    if any(p in texto for p in ["soporte", "help desk", "mesa de ayuda", "técnico", "tecnico"]):
        return "Soporte Técnico"

    if any(p in texto for p in ["software", "programador", "desarrollador", "developer", "ingeniero"]):
        return "Desarrollo de Software"

    return "Otros"


def main():
    print("=" * 60)
    print("STAGING - CLASIFICACIÓN DE ROLES")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    df["categoria_rol"] = df.apply(
        lambda row: clasificar_rol(
            row.get("titulo_oferta"),
            row.get("descripcion_raw")
        ),
        axis=1
    )

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Registros procesados: {len(df)}")
    print()
    print("Distribución por categoría:")
    print(df["categoria_rol"].value_counts())
    print()
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()