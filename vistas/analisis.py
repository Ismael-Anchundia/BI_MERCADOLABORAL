import streamlit as st
import plotly.express as px

from dashboard.estilos import aplicar_estilos

aplicar_estilos()

from dashboard.consultas import (
    obtener_anios_disponibles,
    obtener_paises_disponibles,
    obtener_modalidades_disponibles,
    obtener_salario_promedio_por_ciudad,
    obtener_tecnologias_por_modalidad,
    obtener_ofertas_por_categoria_rol,
    obtener_detalle_ofertas,
)


st.markdown(
    """
    <h1>
        Análisis
        <span style="color:#A78BFA;">
            Detallado
        </span>
    </h1>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Exploración comparativa del mercado laboral tecnológico "
    "según ubicación, modalidad y tecnologías demandadas."
)


anios_disponibles = obtener_anios_disponibles()
paises_disponibles = obtener_paises_disponibles()
modalidades_disponibles = obtener_modalidades_disponibles()

st.markdown("### Filtros de análisis")

col_filtro_1, col_filtro_2, col_filtro_3 = st.columns(3)

with col_filtro_1:
    anio_seleccionado = st.selectbox(
        "Año",
        options=["Todos"] + anios_disponibles,
        key="analisis_anio",
    )

with col_filtro_2:
    pais_seleccionado = st.selectbox(
        "País",
        options=["Todos"] + paises_disponibles,
        key="analisis_pais",
    )

with col_filtro_3:
    modalidad_seleccionada = st.selectbox(
        "Modalidad",
        options=["Todas"] + modalidades_disponibles,
        key="analisis_modalidad",
    )


salarios_ciudad = obtener_salario_promedio_por_ciudad(
    anio=anio_seleccionado,
    pais=pais_seleccionado,
    modalidad=modalidad_seleccionada,
    limite=10,
)

tecnologias_modalidad = obtener_tecnologias_por_modalidad(
    anio=anio_seleccionado,
    pais=pais_seleccionado,
    modalidad=modalidad_seleccionada,
    limite=12,
)

ofertas_por_rol = obtener_ofertas_por_categoria_rol(
    anio=anio_seleccionado,
    pais=pais_seleccionado,
    modalidad=modalidad_seleccionada,
)

detalle_ofertas = obtener_detalle_ofertas(
    anio=anio_seleccionado,
    pais=pais_seleccionado,
    modalidad=modalidad_seleccionada,
    limite=100,
)


st.markdown("---")

col_grafico_1, col_grafico_2 = st.columns(
    [1, 1],
    gap="large",
)


with col_grafico_1:
    st.subheader("Salario promedio por ciudad")

    if salarios_ciudad.empty:
        st.warning(
            "No existen datos salariales disponibles "
            "para los filtros seleccionados."
        )
    else:
        salarios_ciudad = salarios_ciudad.sort_values(
            by="salario_promedio",
            ascending=True,
        )

        figura_salarios_ciudad = px.bar(
            salarios_ciudad,
            x="salario_promedio",
            y="ciudad",
            orientation="h",
            text="salario_promedio",
            custom_data=["total_ofertas"],
            labels={
                "salario_promedio": "Salario promedio (USD)",
                "ciudad": "Ciudad",
            },
        )

        figura_salarios_ciudad.update_traces(
            texttemplate="$%{text:.2f}",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Salario promedio: $%{x:.2f}<br>"
                "Ofertas con salario: %{customdata[0]}"
                "<extra></extra>"
            ),
        )

        figura_salarios_ciudad.update_layout(
            height=470,
            showlegend=False,
            xaxis_title="Salario promedio (USD)",
            yaxis_title=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#EDE9FE",
            margin=dict(
                l=20,
                r=45,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            figura_salarios_ciudad,
            use_container_width=True,
        )


with col_grafico_2:
    st.subheader("Tecnologías según modalidad")

    if tecnologias_modalidad.empty:
        st.warning(
            "No existen tecnologías disponibles "
            "para los filtros seleccionados."
        )
    else:
        tecnologias_modalidad = tecnologias_modalidad.sort_values(
            by="total_ofertas",
            ascending=True,
        )

        figura_tecnologias_modalidad = px.bar(
            tecnologias_modalidad,
            x="total_ofertas",
            y="nombre_tecnologia",
            color="modalidad",
            orientation="h",
            text="total_ofertas",
            labels={
                "total_ofertas": "Número de ofertas",
                "nombre_tecnologia": "Tecnología",
                "modalidad": "Modalidad",
            },
        )

        figura_tecnologias_modalidad.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Ofertas: %{x}<br>"
                "Modalidad: %{fullData.name}"
                "<extra></extra>"
            ),
        )

        figura_tecnologias_modalidad.update_layout(
            height=470,
            xaxis_title="Número de ofertas",
            yaxis_title=None,
            legend_title_text="Modalidad",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#EDE9FE",
            margin=dict(
                l=20,
                r=25,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            figura_tecnologias_modalidad,
            use_container_width=True,
        )

st.markdown("---")
st.subheader("Detalle de ofertas laborales")

if detalle_ofertas.empty:
    st.warning(
        "No existen registros para los filtros seleccionados."
    )
else:
    detalle_mostrar = detalle_ofertas.rename(
        columns={
            "fecha": "Fecha",
            "pais": "País",
            "ciudad": "Ciudad",
            "categoria_rol": "Categoría",
            "nombre_rol": "Rol",
            "modalidad": "Modalidad",
            "nombre_tecnologia": "Tecnología",
            "salario_usd": "Salario USD",
            "experiencia_anios": "Experiencia (años)",
            "num_vacantes": "Vacantes",
        }
    )

    st.dataframe(
        detalle_mostrar,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fecha": st.column_config.DateColumn(
                format="DD/MM/YYYY",
            ),
            "Salario USD": st.column_config.NumberColumn(
                format="$ %.2f",
            ),
            "Experiencia (años)": st.column_config.NumberColumn(
                format="%.1f",
            ),
            "Vacantes": st.column_config.NumberColumn(
                format="%d",
            ),
        },
    )

    st.caption(
        f"Se muestran {len(detalle_mostrar)} registros "
        f"para los filtros seleccionados."
    )