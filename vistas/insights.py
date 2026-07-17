import streamlit as st

from dashboard import estilos
from dashboard.estilos import (
    mostrar_insight,
)
estilos.aplicar_estilos()

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

mostrar_insight(
    f"La tecnología con mayor presencia en el conjunto analizado es "
    f"<b>{tecnologia_lider}</b>, con "
    f"<b>{total_tecnologia} menciones</b>."
)

mostrar_insight(
    f"La mayor concentración geográfica de oportunidades se encuentra en "
    f"<b>{ciudad_lider}</b>, con "
    f"<b>{total_ciudad} ofertas laborales</b>."
)

mostrar_insight(
    f"La modalidad predominante es "
    f"<b>{modalidad_principal}</b>, con "
    f"<b>{total_modalidad} ofertas registradas</b>."
)

mostrar_insight(
    f"La categoría con mayor remuneración promedio es "
    f"<b>{rol_mejor_pagado}</b>, con un salario medio de "
    f"<b>${salario_rol:,.2f} USD</b>, calculado sobre "
    f"<b>{ofertas_rol} ofertas con información salarial</b>."
)

mostrar_insight(
    f"El mayor crecimiento mensual se registró en "
    f"<b>{periodo_crecimiento}</b>, con una variación de "
    f"<b>{crecimiento_maximo:.2f}%</b> respecto al mes anterior."
)