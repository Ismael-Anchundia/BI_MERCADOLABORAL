import streamlit as st

from dashboard.consultas import (
    obtener_total_ofertas,
    obtener_salario_promedio,
    obtener_modalidad_principal,
    obtener_ciudad_lider,
    obtener_tecnologia_lider,
    obtener_rol_mejor_pagado,
    obtener_mayor_crecimiento_mensual,
)


st.markdown(
    """
    <h1>
        Insights
        <span style="color:#A78BFA;">
            Estratégicos
        </span>
    </h1>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Resumen automático de los principales hallazgos "
    "del mercado laboral tecnológico."
)


total_ofertas = obtener_total_ofertas()
salario_promedio = obtener_salario_promedio()
modalidad_principal, total_modalidad = obtener_modalidad_principal()
ciudad_lider, total_ciudad = obtener_ciudad_lider()
tecnologia_lider, total_tecnologia = obtener_tecnologia_lider()
rol_mejor_pagado, salario_rol, ofertas_rol = obtener_rol_mejor_pagado()
periodo_crecimiento, crecimiento_maximo = (
    obtener_mayor_crecimiento_mensual()
)


st.markdown("## Principales hallazgos")

columna_1, columna_2, columna_3 = st.columns(3)

with columna_1:
    st.metric(
        label="Tecnología líder",
        value=tecnologia_lider,
        delta=f"{total_tecnologia} menciones",
    )

with columna_2:
    st.metric(
        label="Ciudad líder",
        value=ciudad_lider,
        delta=f"{total_ciudad} ofertas",
    )

with columna_3:
    st.metric(
        label="Modalidad principal",
        value=modalidad_principal,
        delta=f"{total_modalidad} ofertas",
    )


columna_4, columna_5, columna_6 = st.columns(3)

with columna_4:
    st.metric(
        label="Rol mejor pagado",
        value=rol_mejor_pagado,
        delta=f"${salario_rol:,.2f}",
    )

with columna_5:
    st.metric(
        label="Mayor crecimiento mensual",
        value=f"{crecimiento_maximo:.2f}%",
        delta=periodo_crecimiento,
    )

with columna_6:
    st.metric(
        label="Salario promedio general",
        value=f"${salario_promedio:,.2f}",
        delta=f"{total_ofertas} registros",
    )


st.markdown("---")
st.markdown("## Interpretación ejecutiva")

st.info(
    f"La tecnología con mayor presencia en el conjunto analizado es "
    f"**{tecnologia_lider}**, con **{total_tecnologia} menciones**."
)

st.info(
    f"La mayor concentración geográfica de oportunidades se encuentra en "
    f"**{ciudad_lider}**, con **{total_ciudad} ofertas laborales**."
)

st.info(
    f"La modalidad predominante es **{modalidad_principal}**, "
    f"con **{total_modalidad} ofertas registradas**."
)

st.info(
    f"La categoría con mayor remuneración promedio es "
    f"**{rol_mejor_pagado}**, con un salario medio de "
    f"**${salario_rol:,.2f} USD**, calculado sobre "
    f"**{ofertas_rol} ofertas con información salarial**."
)

st.info(
    f"El mayor crecimiento mensual se registró en "
    f"**{periodo_crecimiento}**, con una variación de "
    f"**{crecimiento_maximo:.2f}%** respecto al mes anterior."
)