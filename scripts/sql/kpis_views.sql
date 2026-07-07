-- ============================================================
-- ENTREGABLE 4 - FRAMEWORK DE KPIs
-- Data Warehouse: dw_ofertas
-- ============================================================

-- KPI 1: Salario promedio por rol tecnológico
CREATE OR REPLACE VIEW dw_ofertas.vw_kpi_salario_promedio_rol AS
SELECT
    dr.categoria_rol,
    COUNT(fo.id_hecho) AS total_ofertas_con_salario,
    ROUND(AVG(fo.salario_usd), 2) AS salario_promedio_usd,
    ROUND(MIN(fo.salario_usd), 2) AS salario_minimo_usd,
    ROUND(MAX(fo.salario_usd), 2) AS salario_maximo_usd
FROM dw_ofertas.fact_ofertas_laborales fo
JOIN dw_ofertas.dim_rol dr
    ON fo.id_rol = dr.id_rol
WHERE fo.salario_usd IS NOT NULL
GROUP BY dr.categoria_rol
ORDER BY salario_promedio_usd DESC;


-- KPI 2: Porcentaje de ofertas por modalidad
CREATE OR REPLACE VIEW dw_ofertas.vw_kpi_modalidad AS
SELECT
    dm.modalidad,
    COUNT(fo.id_hecho) AS total_ofertas,
    ROUND(
        COUNT(fo.id_hecho) * 100.0 / SUM(COUNT(fo.id_hecho)) OVER (),
        2
    ) AS porcentaje
FROM dw_ofertas.fact_ofertas_laborales fo
JOIN dw_ofertas.dim_modalidad dm
    ON fo.id_modalidad = dm.id_modalidad
GROUP BY dm.modalidad
ORDER BY total_ofertas DESC;


-- KPI 3: Participación porcentual de tecnologías identificadas
CREATE OR REPLACE VIEW dw_ofertas.vw_kpi_participacion_tecnologias AS
SELECT
    dtec.nombre_tecnologia,
    dtec.categoria_tecnologia,
    COUNT(fo.id_hecho) AS total_menciones,
    ROUND(
        COUNT(fo.id_hecho) * 100.0 / SUM(COUNT(fo.id_hecho)) OVER (),
        2
    ) AS porcentaje_participacion
FROM dw_ofertas.fact_ofertas_laborales fo
JOIN dw_ofertas.dim_tecnologia dtec
    ON fo.id_tecnologia = dtec.id_tecnologia
GROUP BY
    dtec.nombre_tecnologia,
    dtec.categoria_tecnologia
ORDER BY total_menciones DESC;


-- KPI 4: Participación porcentual de vacantes por ciudad
CREATE OR REPLACE VIEW dw_ofertas.vw_kpi_participacion_ciudades AS
SELECT
    dc.ciudad,
    dc.provincia,
    dc.pais,
    COUNT(fo.id_hecho) AS total_ofertas,
    ROUND(
        COUNT(fo.id_hecho) * 100.0 / SUM(COUNT(fo.id_hecho)) OVER (),
        2
    ) AS porcentaje_participacion
FROM dw_ofertas.fact_ofertas_laborales fo
JOIN dw_ofertas.dim_ciudad dc
    ON fo.id_ciudad = dc.id_ciudad
GROUP BY
    dc.ciudad,
    dc.provincia,
    dc.pais
ORDER BY total_ofertas DESC;


-- KPI 5: Crecimiento mensual de ofertas laborales
CREATE OR REPLACE VIEW dw_ofertas.vw_kpi_crecimiento_mensual AS
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
calculo_crecimiento AS (
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
    anio,
    mes,
    total_ofertas,
    ofertas_mes_anterior,
    CASE
        WHEN ofertas_mes_anterior IS NULL THEN NULL
        WHEN ofertas_mes_anterior = 0 THEN NULL
        ELSE ROUND(
            ((total_ofertas - ofertas_mes_anterior) * 100.0 / ofertas_mes_anterior),
            2
        )
    END AS porcentaje_crecimiento
FROM calculo_crecimiento
ORDER BY anio, mes;