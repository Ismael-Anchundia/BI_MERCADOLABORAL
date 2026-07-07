import pandas as pd
import psycopg2
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
CSV_FILE = BASE_DIR / "data" / "staging" / "ofertas_staging_dw.csv"


DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "database": "bi_ofertas_dw",
    "user": "postgres",
    "password": "damaris"
}

SCHEMA = "dw_ofertas"


def limpiar(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return None
    return str(valor).strip()


def id_tiempo(fecha):
    fecha = pd.to_datetime(fecha)
    return int(fecha.strftime("%Y%m%d"))


def ejecutar_insert_dimensiones(cursor, df):
    print("Cargando dimensiones...")

    # DimTiempo
    fechas = pd.to_datetime(df["fecha_publicacion"].dropna().unique())
    for fecha in fechas:
        cursor.execute(f"""
            INSERT INTO {SCHEMA}.dim_tiempo
            (id_tiempo, fecha, dia, mes, trimestre, anio)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_tiempo) DO NOTHING;
        """, (
            int(fecha.strftime("%Y%m%d")),
            fecha.date(),
            fecha.day,
            fecha.month,
            ((fecha.month - 1) // 3) + 1,
            fecha.year
        ))

    # DimFuente
    for _, row in df[["fuente", "tipo_fuente"]].drop_duplicates().iterrows():
        cursor.execute(f"""
            INSERT INTO {SCHEMA}.dim_fuente
            (nombre_fuente, tipo_fuente)
            VALUES (%s, %s)
            ON CONFLICT (nombre_fuente) DO NOTHING;
        """, (
            limpiar(row["fuente"]) or "No especificado",
            limpiar(row["tipo_fuente"]) or "Scraping"
        ))

    # DimCiudad
    for _, row in df[["ciudad_limpia", "provincia", "pais"]].drop_duplicates().iterrows():
        cursor.execute(f"""
            INSERT INTO {SCHEMA}.dim_ciudad
            (ciudad, provincia, pais)
            VALUES (%s, %s, %s)
            ON CONFLICT (ciudad, provincia, pais) DO NOTHING;
        """, (
            limpiar(row["ciudad_limpia"]) or "No especificado",
            limpiar(row["provincia"]) or "No especificado",
            limpiar(row["pais"]) or "No especificado"
        ))

    # DimRol
    for _, row in df[["nombre_rol", "categoria_rol"]].drop_duplicates().iterrows():
        cursor.execute(f"""
            INSERT INTO {SCHEMA}.dim_rol
            (nombre_rol, categoria_rol)
            VALUES (%s, %s)
            ON CONFLICT (nombre_rol) DO NOTHING;
        """, (
            limpiar(row["nombre_rol"]) or "No especificado",
            limpiar(row["categoria_rol"]) or "Otros"
        ))

    # DimModalidad
    for modalidad in df["modalidad"].dropna().drop_duplicates():
        cursor.execute(f"""
            INSERT INTO {SCHEMA}.dim_modalidad
            (modalidad)
            VALUES (%s)
            ON CONFLICT (modalidad) DO NOTHING;
        """, (
            limpiar(modalidad) or "No especificado",
        ))

    # DimTecnologia
    for _, row in df[["nombre_tecnologia", "categoria_tecnologia"]].drop_duplicates().iterrows():
        cursor.execute(f"""
            INSERT INTO {SCHEMA}.dim_tecnologia
            (nombre_tecnologia, categoria_tecnologia)
            VALUES (%s, %s)
            ON CONFLICT (nombre_tecnologia) DO NOTHING;
        """, (
            limpiar(row["nombre_tecnologia"]) or "No especificado",
            limpiar(row["categoria_tecnologia"]) or "No especificado"
        ))

    print("Dimensiones cargadas correctamente.")


def obtener_id(cursor, tabla, campo_id, condiciones):
    where = " AND ".join([f"{campo} = %s" for campo in condiciones.keys()])
    valores = list(condiciones.values())

    cursor.execute(f"""
        SELECT {campo_id}
        FROM {SCHEMA}.{tabla}
        WHERE {where}
        LIMIT 1;
    """, valores)

    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    return None


def cargar_hechos(cursor, df):
    print("Cargando tabla de hechos...")

    insertados = 0
    omitidos = 0

    for _, row in df.iterrows():
        try:
            fecha = pd.to_datetime(row["fecha_publicacion"])

            id_t = int(fecha.strftime("%Y%m%d"))

            id_f = obtener_id(cursor, "dim_fuente", "id_fuente", {
                "nombre_fuente": limpiar(row["fuente"]) or "No especificado"
            })

            id_c = obtener_id(cursor, "dim_ciudad", "id_ciudad", {
                "ciudad": limpiar(row["ciudad_limpia"]) or "No especificado",
                "provincia": limpiar(row["provincia"]) or "No especificado",
                "pais": limpiar(row["pais"]) or "No especificado"
            })

            id_r = obtener_id(cursor, "dim_rol", "id_rol", {
                "nombre_rol": limpiar(row["nombre_rol"]) or "No especificado"
            })

            id_m = obtener_id(cursor, "dim_modalidad", "id_modalidad", {
                "modalidad": limpiar(row["modalidad"]) or "No especificado"
            })

            id_tec = obtener_id(cursor, "dim_tecnologia", "id_tecnologia", {
                "nombre_tecnologia": limpiar(row["nombre_tecnologia"]) or "No especificado"
            })

            salario = row["salario_usd"]
            salario = None if pd.isna(salario) else float(salario)

            num_vacantes = row["num_vacantes"]
            num_vacantes = 1 if pd.isna(num_vacantes) else int(num_vacantes)

            experiencia = row["experiencia_anios"]
            experiencia = None if pd.isna(experiencia) else int(experiencia)

            cursor.execute(f"""
                INSERT INTO {SCHEMA}.fact_ofertas_laborales
                (
                    id_tiempo,
                    id_fuente,
                    id_ciudad,
                    id_rol,
                    id_modalidad,
                    id_tecnologia,
                    salario_usd,
                    num_vacantes,
                    experiencia_anios
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                id_t,
                id_f,
                id_c,
                id_r,
                id_m,
                id_tec,
                salario,
                num_vacantes,
                experiencia
            ))

            insertados += 1

        except Exception as e:
            omitidos += 1
            print(f"Registro omitido: {e}")

    print(f"Hechos insertados: {insertados}")
    print(f"Hechos omitidos: {omitidos}")


def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {CSV_FILE}")

    df = pd.read_csv(CSV_FILE)

    print("=" * 70)
    print("CARGA DEL DATA WAREHOUSE EN POSTGRESQL")
    print("=" * 70)
    print(f"Archivo staging: {CSV_FILE}")
    print(f"Registros leídos: {len(df)}")

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        ejecutar_insert_dimensiones(cursor, df)
        cargar_hechos(cursor, df)

        conn.commit()

        print("=" * 70)
        print("CARGA FINALIZADA CORRECTAMENTE")
        print("=" * 70)

    except Exception as e:
        conn.rollback()
        print("Error durante la carga. Se hizo rollback.")
        print(e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()