import pandas as pd
import streamlit as st


def obtener_conexion():
    """
    Devuelve la conexión SQL configurada en
    .streamlit/secrets.toml.
    """
    return st.connection(
        "postgresql",
        type="sql",
    )


def probar_conexion() -> bool:
    """
    Ejecuta una consulta mínima para comprobar que
    PostgreSQL está disponible.
    """
    try:
        conexion = obtener_conexion()

        resultado = conexion.query(
            "SELECT 1 AS conexion_exitosa;",
            ttl=0,
        )

        return (
            not resultado.empty
            and resultado.iloc[0]["conexion_exitosa"] == 1
        )

    except Exception:
        return False


def ejecutar_consulta(
    consulta: str,
    ttl: int = 300,
    params: dict | None = None,
) -> pd.DataFrame:
    """
    Ejecuta una consulta SELECT y devuelve un DataFrame.

    ttl:
        Tiempo en segundos durante el cual Streamlit
        conserva el resultado en caché.

    params:
        Diccionario opcional con parámetros para la consulta SQL.
    """
    conexion = obtener_conexion()

    return conexion.query(
        consulta,
        ttl=ttl,
        params=params,
    )