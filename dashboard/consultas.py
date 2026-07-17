import pandas as pd

from dashboard.conexion import ejecutar_consulta


def obtener_total_ofertas(
    anio=None,
    pais=None,
    modalidad=None,
) -> int:
    condiciones = []
    parametros = {}

    if anio not in (None, "Todos"):
        condiciones.append("dti.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = ""

    if condiciones:
        clausula_where = "WHERE " + " AND ".join(condiciones)

    consulta = f"""
        SELECT
            COUNT(fo.id_hecho) AS total_ofertas
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_tiempo dti
            ON fo.id_tiempo = dti.id_tiempo
        JOIN dw_ofertas.dim_ciudad dc
            ON fo.id_ciudad = dc.id_ciudad
        JOIN dw_ofertas.dim_modalidad dm
            ON fo.id_modalidad = dm.id_modalidad
        {clausula_where};
    """

    resultado: pd.DataFrame = ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

    if resultado.empty:
        return 0

    return int(resultado.iloc[0]["total_ofertas"])

def obtener_salario_promedio(
    anio=None,
    pais=None,
    modalidad=None,
) -> float:
    condiciones = [
        "fo.salario_usd IS NOT NULL",
    ]
    parametros = {}

    if anio not in (None, "Todos"):
        condiciones.append("dti.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = "WHERE " + " AND ".join(condiciones)

    consulta = f"""
        SELECT
            ROUND(
                AVG(fo.salario_usd),
                2
            ) AS salario_promedio
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_tiempo dti
            ON fo.id_tiempo = dti.id_tiempo
        JOIN dw_ofertas.dim_ciudad dc
            ON fo.id_ciudad = dc.id_ciudad
        JOIN dw_ofertas.dim_modalidad dm
            ON fo.id_modalidad = dm.id_modalidad
        {clausula_where};
    """

    resultado: pd.DataFrame = ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

    if (
        resultado.empty
        or pd.isna(resultado.iloc[0]["salario_promedio"])
    ):
        return 0.0

    return float(resultado.iloc[0]["salario_promedio"])


def obtener_modalidad_principal(
    anio=None,
    pais=None,
) -> tuple[str, int]:
    condiciones = [
        "dm.modalidad <> 'No especificado'",
    ]
    parametros = {}

    if anio not in (None, "Todos"):
        condiciones.append("dti.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    clausula_where = "WHERE " + " AND ".join(condiciones)

    consulta = f"""
        SELECT
            dm.modalidad,
            COUNT(fo.id_hecho) AS total_ofertas
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_modalidad dm
            ON fo.id_modalidad = dm.id_modalidad
        JOIN dw_ofertas.dim_tiempo dti
            ON fo.id_tiempo = dti.id_tiempo
        JOIN dw_ofertas.dim_ciudad dc
            ON fo.id_ciudad = dc.id_ciudad
        {clausula_where}
        GROUP BY dm.modalidad
        ORDER BY total_ofertas DESC
        LIMIT 1;
    """

    resultado: pd.DataFrame = ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

    if resultado.empty:
        return "No disponible", 0

    modalidad = str(resultado.iloc[0]["modalidad"])
    total = int(resultado.iloc[0]["total_ofertas"])

    return modalidad, total

def obtener_ciudad_lider(
    anio=None,
    pais=None,
    modalidad=None,
) -> tuple[str, int]:
    condiciones = [
        "dc.ciudad <> 'No especificado'",
    ]
    parametros = {}

    if anio not in (None, "Todos"):
        condiciones.append("dti.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = "WHERE " + " AND ".join(condiciones)

    consulta = f"""
        SELECT
            dc.ciudad,
            COUNT(fo.id_hecho) AS total_ofertas
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_ciudad dc
            ON fo.id_ciudad = dc.id_ciudad
        JOIN dw_ofertas.dim_tiempo dti
            ON fo.id_tiempo = dti.id_tiempo
        JOIN dw_ofertas.dim_modalidad dm
            ON fo.id_modalidad = dm.id_modalidad
        {clausula_where}
        GROUP BY dc.ciudad
        ORDER BY total_ofertas DESC
        LIMIT 1;
    """

    resultado: pd.DataFrame = ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

    if resultado.empty:
        return "No disponible", 0

    ciudad = str(resultado.iloc[0]["ciudad"])
    total = int(resultado.iloc[0]["total_ofertas"])

    return ciudad, total

def obtener_tecnologia_lider(
    anio=None,
    pais=None,
    modalidad=None,
) -> tuple[str, int]:
    condiciones = [
        "dtec.nombre_tecnologia <> 'No especificado'",
    ]
    parametros = {}

    if anio not in (None, "Todos"):
        condiciones.append("dti.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = "WHERE " + " AND ".join(condiciones)

    consulta = f"""
        SELECT
            dtec.nombre_tecnologia,
            COUNT(fo.id_hecho) AS total_menciones
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_tecnologia dtec
            ON fo.id_tecnologia = dtec.id_tecnologia
        JOIN dw_ofertas.dim_tiempo dti
            ON fo.id_tiempo = dti.id_tiempo
        JOIN dw_ofertas.dim_ciudad dc
            ON fo.id_ciudad = dc.id_ciudad
        JOIN dw_ofertas.dim_modalidad dm
            ON fo.id_modalidad = dm.id_modalidad
        {clausula_where}
        GROUP BY dtec.nombre_tecnologia
        ORDER BY total_menciones DESC
        LIMIT 1;
    """

    resultado: pd.DataFrame = ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

    if resultado.empty:
        return "No disponible", 0

    tecnologia = str(
        resultado.iloc[0]["nombre_tecnologia"]
    )
    total = int(
        resultado.iloc[0]["total_menciones"]
    )

    return tecnologia, total

def obtener_top_tecnologias(
    limite: int = 10,
    anio=None,
    pais=None,
    modalidad=None,
) -> pd.DataFrame:
    condiciones = [
        "dtec.nombre_tecnologia <> 'No especificado'"
    ]

    parametros = {
        "limite": int(limite),
    }

    if anio not in (None, "Todos"):
        condiciones.append("dti.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = "WHERE " + " AND ".join(condiciones)

    consulta = f"""
        WITH datos_filtrados AS (
            SELECT
                fo.id_hecho,
                dtec.nombre_tecnologia
            FROM dw_ofertas.fact_ofertas_laborales fo
            JOIN dw_ofertas.dim_tecnologia dtec
                ON fo.id_tecnologia = dtec.id_tecnologia
            JOIN dw_ofertas.dim_tiempo dti
                ON fo.id_tiempo = dti.id_tiempo
            JOIN dw_ofertas.dim_ciudad dc
                ON fo.id_ciudad = dc.id_ciudad
            JOIN dw_ofertas.dim_modalidad dm
                ON fo.id_modalidad = dm.id_modalidad
            {clausula_where}
        ),
        total_filtrado AS (
            SELECT COUNT(*) AS total_ofertas
            FROM datos_filtrados
        )
        SELECT
            df.nombre_tecnologia,
            COUNT(df.id_hecho) AS total_menciones,
            ROUND(
                COUNT(df.id_hecho) * 100.0
                / NULLIF(tf.total_ofertas, 0),
                2
            ) AS porcentaje_participacion
        FROM datos_filtrados df
        CROSS JOIN total_filtrado tf
        GROUP BY
            df.nombre_tecnologia,
            tf.total_ofertas
        ORDER BY total_menciones DESC
        LIMIT :limite;
    """

    return ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

def obtener_distribucion_modalidades(
    anio=None,
    pais=None,
) -> pd.DataFrame:
    condiciones = []
    parametros = {}

    if anio not in (None, "Todos"):
        condiciones.append("dt.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    clausula_where = ""

    if condiciones:
        clausula_where = (
            "WHERE " + " AND ".join(condiciones)
        )

    consulta = f"""
        WITH modalidades_filtradas AS (
            SELECT
                fo.id_hecho,
                dm.modalidad
            FROM dw_ofertas.fact_ofertas_laborales fo
            JOIN dw_ofertas.dim_modalidad dm
                ON fo.id_modalidad = dm.id_modalidad
            JOIN dw_ofertas.dim_tiempo dt
                ON fo.id_tiempo = dt.id_tiempo
            JOIN dw_ofertas.dim_ciudad dc
                ON fo.id_ciudad = dc.id_ciudad
            {clausula_where}
        ),
        total_filtrado AS (
            SELECT COUNT(*) AS total_ofertas
            FROM modalidades_filtradas
        )
        SELECT
            mf.modalidad,
            COUNT(mf.id_hecho) AS total_ofertas,
            ROUND(
                COUNT(mf.id_hecho) * 100.0
                / NULLIF(tf.total_ofertas, 0),
                2
            ) AS porcentaje
        FROM modalidades_filtradas mf
        CROSS JOIN total_filtrado tf
        GROUP BY
            mf.modalidad,
            tf.total_ofertas
        ORDER BY total_ofertas DESC;
    """

    return ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

def obtener_evolucion_mensual() -> pd.DataFrame:
    consulta = """
        SELECT
            dt.anio,
            dt.mes,
            TO_CHAR(
                MAKE_DATE(dt.anio, dt.mes, 1),
                'YYYY-MM'
            ) AS periodo,
            COUNT(fo.id_hecho) AS total_ofertas
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_tiempo dt
            ON fo.id_tiempo = dt.id_tiempo
        GROUP BY
            dt.anio,
            dt.mes
        ORDER BY
            dt.anio ASC,
            dt.mes ASC;
    """

    return ejecutar_consulta(
        consulta,
        ttl=300,
    )

def obtener_anios_disponibles() -> list[int]:
    consulta = """
        SELECT DISTINCT anio
        FROM dw_ofertas.dim_tiempo
        ORDER BY anio ASC;
    """

    resultado = ejecutar_consulta(
        consulta,
        ttl=300,
    )

    if resultado.empty:
        return []

    return resultado["anio"].astype(int).tolist()


def obtener_paises_disponibles() -> list[str]:
    consulta = """
        SELECT DISTINCT pais
        FROM dw_ofertas.dim_ciudad
        WHERE pais IS NOT NULL
          AND pais <> 'No especificado'
        ORDER BY pais ASC;
    """

    resultado = ejecutar_consulta(
        consulta,
        ttl=300,
    )

    if resultado.empty:
        return []

    return resultado["pais"].astype(str).tolist()


def obtener_modalidades_disponibles() -> list[str]:
    consulta = """
        SELECT DISTINCT modalidad
        FROM dw_ofertas.dim_modalidad
        WHERE modalidad IS NOT NULL
        ORDER BY modalidad ASC;
    """

    resultado = ejecutar_consulta(
        consulta,
        ttl=300,
    )

    if resultado.empty:
        return []

    return resultado["modalidad"].astype(str).tolist()

def construir_filtros(
    anio=None,
    pais=None,
    modalidad=None,
) -> tuple[str, dict]:
    condiciones = []
    parametros = {}

    if anio not in (None, "Todos"):
        condiciones.append("dt.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    if not condiciones:
        return "", parametros

    clausula_where = "WHERE " + " AND ".join(condiciones)

    return clausula_where, parametros

def obtener_participacion_ciudades(
    anio=None,
    pais=None,
    modalidad=None,
    limite: int = 10,
) -> pd.DataFrame:
    condiciones = [
        "dc.ciudad IS NOT NULL",
        "dc.ciudad <> 'No especificado'",
    ]

    parametros = {
        "limite": int(limite),
    }

    if anio not in (None, "Todos"):
        condiciones.append("dt.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = "WHERE " + " AND ".join(condiciones)

    consulta = f"""
        WITH ofertas_filtradas AS (
            SELECT
                fo.id_hecho,
                dc.ciudad
            FROM dw_ofertas.fact_ofertas_laborales fo
            JOIN dw_ofertas.dim_ciudad dc
                ON fo.id_ciudad = dc.id_ciudad
            JOIN dw_ofertas.dim_tiempo dt
                ON fo.id_tiempo = dt.id_tiempo
            JOIN dw_ofertas.dim_modalidad dm
                ON fo.id_modalidad = dm.id_modalidad
            {clausula_where}
        ),
        total_filtrado AS (
            SELECT COUNT(*) AS total_ofertas
            FROM ofertas_filtradas
        )
        SELECT
            ofi.ciudad,
            COUNT(ofi.id_hecho) AS total_ofertas,
            ROUND(
                COUNT(ofi.id_hecho) * 100.0
                / NULLIF(tf.total_ofertas, 0),
                2
            ) AS porcentaje_participacion
        FROM ofertas_filtradas ofi
        CROSS JOIN total_filtrado tf
        GROUP BY
            ofi.ciudad,
            tf.total_ofertas
        ORDER BY total_ofertas DESC
        LIMIT :limite;
    """

    return ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

def obtener_salario_promedio_por_rol(
    anio=None,
    pais=None,
    modalidad=None,
) -> pd.DataFrame:

    condiciones = [
        "fo.salario_usd IS NOT NULL"
    ]

    parametros = {}

    if anio not in (None, "Todos"):
        condiciones.append("dt.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = "WHERE " + " AND ".join(condiciones)

    consulta = f"""
        SELECT
            dr.categoria_rol,
            ROUND(
                AVG(fo.salario_usd),
                2
            ) AS salario_promedio,
            COUNT(*) AS total_ofertas
        FROM dw_ofertas.fact_ofertas_laborales fo

        JOIN dw_ofertas.dim_rol dr
            ON fo.id_rol = dr.id_rol

        JOIN dw_ofertas.dim_tiempo dt
            ON fo.id_tiempo = dt.id_tiempo

        JOIN dw_ofertas.dim_ciudad dc
            ON fo.id_ciudad = dc.id_ciudad

        JOIN dw_ofertas.dim_modalidad dm
            ON fo.id_modalidad = dm.id_modalidad

        {clausula_where}

        GROUP BY dr.categoria_rol

        ORDER BY salario_promedio DESC;
    """

    return ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

#Segunda pestaña
def obtener_salario_promedio_por_ciudad(
    anio=None,
    pais=None,
    modalidad=None,
    limite: int = 10,
) -> pd.DataFrame:
    condiciones = [
        "fo.salario_usd IS NOT NULL",
        "dc.ciudad IS NOT NULL",
        "dc.ciudad <> 'No especificado'",
    ]

    parametros = {
        "limite": int(limite),
    }

    if anio not in (None, "Todos"):
        condiciones.append("dt.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = "WHERE " + " AND ".join(condiciones)

    consulta = f"""
        SELECT
            dc.ciudad,
            ROUND(
                AVG(fo.salario_usd),
                2
            ) AS salario_promedio,
            COUNT(*) AS total_ofertas
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_ciudad dc
            ON fo.id_ciudad = dc.id_ciudad
        JOIN dw_ofertas.dim_tiempo dt
            ON fo.id_tiempo = dt.id_tiempo
        JOIN dw_ofertas.dim_modalidad dm
            ON fo.id_modalidad = dm.id_modalidad
        {clausula_where}
        GROUP BY dc.ciudad
        ORDER BY salario_promedio DESC
        LIMIT :limite;
    """

    return ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

def obtener_tecnologias_por_modalidad(
    anio=None,
    pais=None,
    modalidad=None,
    limite: int = 12,
) -> pd.DataFrame:
    condiciones = [
        "dtec.nombre_tecnologia <> 'No especificado'"
    ]

    parametros = {
        "limite": int(limite),
    }

    if anio not in (None, "Todos"):
        condiciones.append("dt.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = "WHERE " + " AND ".join(condiciones)

    consulta = f"""
        SELECT
            dtec.nombre_tecnologia,
            dm.modalidad,
            COUNT(fo.id_hecho) AS total_ofertas
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_tecnologia dtec
            ON fo.id_tecnologia = dtec.id_tecnologia
        JOIN dw_ofertas.dim_modalidad dm
            ON fo.id_modalidad = dm.id_modalidad
        JOIN dw_ofertas.dim_tiempo dt
            ON fo.id_tiempo = dt.id_tiempo
        JOIN dw_ofertas.dim_ciudad dc
            ON fo.id_ciudad = dc.id_ciudad
        {clausula_where}
        GROUP BY
            dtec.nombre_tecnologia,
            dm.modalidad
        ORDER BY total_ofertas DESC
        LIMIT :limite;
    """

    return ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

def obtener_ofertas_por_categoria_rol(
    anio=None,
    pais=None,
    modalidad=None,
) -> pd.DataFrame:
    condiciones = []
    parametros = {}

    if anio not in (None, "Todos"):
        condiciones.append("dt.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = ""

    if condiciones:
        clausula_where = (
            "WHERE " + " AND ".join(condiciones)
        )

    consulta = f"""
        SELECT
            dr.categoria_rol,
            COUNT(fo.id_hecho) AS total_ofertas
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_rol dr
            ON fo.id_rol = dr.id_rol
        JOIN dw_ofertas.dim_tiempo dt
            ON fo.id_tiempo = dt.id_tiempo
        JOIN dw_ofertas.dim_ciudad dc
            ON fo.id_ciudad = dc.id_ciudad
        JOIN dw_ofertas.dim_modalidad dm
            ON fo.id_modalidad = dm.id_modalidad
        {clausula_where}
        GROUP BY dr.categoria_rol
        ORDER BY total_ofertas DESC;
    """

    return ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

def obtener_detalle_ofertas(
    anio=None,
    pais=None,
    modalidad=None,
    limite: int = 100,
) -> pd.DataFrame:
    condiciones = []
    parametros = {
        "limite": int(limite),
    }

    if anio not in (None, "Todos"):
        condiciones.append("dt.anio = :anio")
        parametros["anio"] = int(anio)

    if pais not in (None, "Todos"):
        condiciones.append("dc.pais = :pais")
        parametros["pais"] = pais

    if modalidad not in (None, "Todas"):
        condiciones.append("dm.modalidad = :modalidad")
        parametros["modalidad"] = modalidad

    clausula_where = ""

    if condiciones:
        clausula_where = (
            "WHERE " + " AND ".join(condiciones)
        )

    consulta = f"""
        SELECT
            dt.fecha,
            dc.pais,
            dc.ciudad,
            dr.categoria_rol,
            dr.nombre_rol,
            dm.modalidad,
            dtec.nombre_tecnologia,
            fo.salario_usd,
            fo.experiencia_anios,
            fo.num_vacantes
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_tiempo dt
            ON fo.id_tiempo = dt.id_tiempo
        JOIN dw_ofertas.dim_ciudad dc
            ON fo.id_ciudad = dc.id_ciudad
        JOIN dw_ofertas.dim_rol dr
            ON fo.id_rol = dr.id_rol
        JOIN dw_ofertas.dim_modalidad dm
            ON fo.id_modalidad = dm.id_modalidad
        JOIN dw_ofertas.dim_tecnologia dtec
            ON fo.id_tecnologia = dtec.id_tecnologia
        {clausula_where}
        ORDER BY dt.fecha DESC
        LIMIT :limite;
    """

    return ejecutar_consulta(
        consulta,
        ttl=300,
        params=parametros,
    )

def obtener_rol_mejor_pagado() -> tuple[str, float, int]:
    consulta = """
        SELECT
            dr.categoria_rol,
            ROUND(AVG(fo.salario_usd), 2) AS salario_promedio,
            COUNT(*) AS total_ofertas
        FROM dw_ofertas.fact_ofertas_laborales fo
        JOIN dw_ofertas.dim_rol dr
            ON fo.id_rol = dr.id_rol
        WHERE fo.salario_usd IS NOT NULL
        GROUP BY dr.categoria_rol
        ORDER BY salario_promedio DESC
        LIMIT 1;
    """

    resultado = ejecutar_consulta(
        consulta,
        ttl=300,
    )

    if resultado.empty:
        return "No disponible", 0.0, 0

    return (
        str(resultado.iloc[0]["categoria_rol"]),
        float(resultado.iloc[0]["salario_promedio"]),
        int(resultado.iloc[0]["total_ofertas"]),
    )


def obtener_mayor_crecimiento_mensual() -> tuple[str, float]:
    consulta = """
        WITH ofertas_mensuales AS (
            SELECT
                dt.anio,
                dt.mes,
                COUNT(fo.id_hecho) AS total_ofertas
            FROM dw_ofertas.fact_ofertas_laborales fo
            JOIN dw_ofertas.dim_tiempo dt
                ON fo.id_tiempo = dt.id_tiempo
            GROUP BY
                dt.anio,
                dt.mes
        ),
        variaciones AS (
            SELECT
                anio,
                mes,
                total_ofertas,
                LAG(total_ofertas) OVER (
                    ORDER BY anio, mes
                ) AS ofertas_mes_anterior
            FROM ofertas_mensuales
        )
        SELECT
            TO_CHAR(
                MAKE_DATE(anio, mes, 1),
                'YYYY-MM'
            ) AS periodo,
            ROUND(
                (
                    total_ofertas - ofertas_mes_anterior
                ) * 100.0
                / NULLIF(ofertas_mes_anterior, 0),
                2
            ) AS crecimiento_porcentual
        FROM variaciones
        WHERE ofertas_mes_anterior IS NOT NULL
        ORDER BY crecimiento_porcentual DESC
        LIMIT 1;
    """

    resultado = ejecutar_consulta(
        consulta,
        ttl=300,
    )

    if resultado.empty:
        return "No disponible", 0.0

    return (
        str(resultado.iloc[0]["periodo"]),
        float(resultado.iloc[0]["crecimiento_porcentual"]),
    )