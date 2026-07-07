SELECT
    dt.anio,
    dt.mes,
    dtec.nombre_tecnologia,
    dm.modalidad,
    COUNT(fo.id_hecho) AS total_ofertas,
    ROUND(AVG(fo.salario_usd), 2) AS salario_promedio
FROM dw_ofertas.fact_ofertas_laborales fo
JOIN dw_ofertas.dim_tiempo dt
    ON fo.id_tiempo = dt.id_tiempo
JOIN dw_ofertas.dim_tecnologia dtec
    ON fo.id_tecnologia = dtec.id_tecnologia
JOIN dw_ofertas.dim_modalidad dm
    ON fo.id_modalidad = dm.id_modalidad
JOIN dw_ofertas.dim_ciudad dc
    ON fo.id_ciudad = dc.id_ciudad
WHERE dc.pais = 'Ecuador'
GROUP BY
    dt.anio,
    dt.mes,
    dtec.nombre_tecnologia,
    dm.modalidad
ORDER BY
    dt.anio,
    dt.mes,
    total_ofertas DESC;

---------------------------------------------

SELECT
    dtec.nombre_tecnologia,
    dtec.categoria_tecnologia,
    COUNT(fo.id_hecho) AS menciones,
    ROUND(
        COUNT(fo.id_hecho) * 100.0 / SUM(COUNT(fo.id_hecho)) OVER (),
        2
    ) AS porcentaje
FROM dw_ofertas.fact_ofertas_laborales fo
JOIN dw_ofertas.dim_tecnologia dtec
    ON fo.id_tecnologia = dtec.id_tecnologia
JOIN dw_ofertas.dim_ciudad dc
    ON fo.id_ciudad = dc.id_ciudad
WHERE dc.pais = 'Ecuador'
GROUP BY
    dtec.nombre_tecnologia,
    dtec.categoria_tecnologia
ORDER BY menciones DESC;

--------------------------------------------------------------------------

SELECT
    dr.categoria_rol,
    dc.ciudad,
    dc.provincia,
    fo.experiencia_anios,
    COUNT(fo.id_hecho) AS total_ofertas,
    ROUND(AVG(fo.salario_usd), 2) AS salario_promedio,
    ROUND(MIN(fo.salario_usd), 2) AS salario_minimo,
    ROUND(MAX(fo.salario_usd), 2) AS salario_maximo
FROM dw_ofertas.fact_ofertas_laborales fo
JOIN dw_ofertas.dim_rol dr
    ON fo.id_rol = dr.id_rol
JOIN dw_ofertas.dim_ciudad dc
    ON fo.id_ciudad = dc.id_ciudad
WHERE dc.pais = 'Ecuador'
  AND fo.salario_usd IS NOT NULL
GROUP BY
    dr.categoria_rol,
    dc.ciudad,
    dc.provincia,
    fo.experiencia_anios
ORDER BY salario_promedio DESC;

------------------------------------------------------

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
JOIN dw_ofertas.dim_ciudad dc
    ON fo.id_ciudad = dc.id_ciudad
WHERE dc.pais = 'Ecuador'
GROUP BY dm.modalidad
ORDER BY total_ofertas DESC;

--------------------------------------------------------------------

SELECT
    dc.ciudad,
    dc.provincia,
    dc.pais,
    COUNT(fo.id_hecho) AS total_ofertas,
    ROUND(
        COUNT(fo.id_hecho) * 100.0 / SUM(COUNT(fo.id_hecho)) OVER (),
        2
    ) AS porcentaje
FROM dw_ofertas.fact_ofertas_laborales fo
JOIN dw_ofertas.dim_ciudad dc
    ON fo.id_ciudad = dc.id_ciudad
WHERE dc.pais = 'Ecuador'
GROUP BY
    dc.ciudad,
    dc.provincia,
    dc.pais
ORDER BY total_ofertas DESC
LIMIT 10;

---------------------------------------------

SELECT
    dt.anio,
    dt.mes,
    dtec.nombre_tecnologia,
    COUNT(fo.id_hecho) AS total_ofertas,
    RANK() OVER (
        PARTITION BY dt.anio, dt.mes
        ORDER BY COUNT(fo.id_hecho) DESC
    ) AS ranking_mensual
FROM dw_ofertas.fact_ofertas_laborales fo
JOIN dw_ofertas.dim_tiempo dt
    ON fo.id_tiempo = dt.id_tiempo
JOIN dw_ofertas.dim_tecnologia dtec
    ON fo.id_tecnologia = dtec.id_tecnologia
JOIN dw_ofertas.dim_ciudad dc
    ON fo.id_ciudad = dc.id_ciudad
WHERE dc.pais = 'Ecuador'
GROUP BY
    dt.anio,
    dt.mes,
    dtec.nombre_tecnologia
ORDER BY
    dt.anio,
    dt.mes,
    ranking_mensual;