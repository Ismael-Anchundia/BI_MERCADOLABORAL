import streamlit as st
import plotly.express as px

st.markdown(
    """
    <style>
    /* Fondo principal */
    .stApp {
        background:
            radial-gradient(
                circle at top left,
                rgba(139, 92, 246, 0.16),
                transparent 32%
            ),
            linear-gradient(
                135deg,
                #100b1f 0%,
                #160f2b 48%,
                #0d0919 100%
            );
        color: #f8f7ff;
    }

    /* Contenedor principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Título principal */
    h1 {
        color: #f8fafc !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
    }

    h1 span {
        color: #ffffff;
    }

    /* Subtítulos */
    h2, h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }

    /* Texto secundario */
    [data-testid="stCaptionContainer"] {
        color: #94a3b8 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #1b1232 0%,
            #100b1f 100%
        );
        border-right: 1px solid rgba(196, 181, 253, 0.16);
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    /* Navegación activa */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(
            90deg,
            #6d28d9,
            #8b5cf6
        );
        border-radius: 10px;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #21183a !important;
        border: 1px solid #493873 !important;
        border-radius: 10px !important;
        color: #f8f7ff !important;
        min-height: 46px;
    }

    div[data-baseweb="select"] span {
        color: #f8fafc !important;
    }

    /* Mensaje de conexión */
    [data-testid="stAlert"] {
        background-color: rgba(16, 185, 129, 0.10);
        border: 1px solid rgba(16, 185, 129, 0.20);
        border-radius: 10px;
        color: #86efac;
    }

    /* Tarjetas KPI */
    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #261b43,
            #1b1432
        );
        border: 1px solid rgba(167, 139, 250, 0.24);
        border-radius: 14px;
        padding: 1.25rem 1rem;
        box-shadow:
            0 12px 32px rgba(5, 2, 15, 0.38),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);
        min-height: 155px;
        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(167, 139, 250, 0.60);
    }

    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-size: 0.92rem;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 750 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #4ade80 !important;
    }

    /* Contenedor de gráficos */
    [data-testid="stPlotlyChart"] {
        background: transparent;
        border: none;
        padding: 0;
        box-shadow: none;
    }

    /* Cajas informativas */
    div[data-testid="stNotification"] {
        border-radius: 10px;
    }

    /* Líneas divisorias */
    hr {
        border-color: rgba(148, 163, 184, 0.18);
    }

    /* Menú desplegable */
    div[role="listbox"] {
        background-color: #261b43 !important;
        color: #f8f7ff !important;
    }

    div[role="option"]:hover {
        background-color: #3b2863 !important;
    }

    div[role="option"]:hover {
        background-color: #1e3a5f !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def aplicar_estilo_grafico(
    figura,
    altura: int = 430,
):
    figura.update_layout(
        height=altura,
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#EDE9FE",
            family="Arial",
        ),
        legend=dict(
            font=dict(
                color="#DDD6FE",
            ),
            title_font=dict(
                color="#F5F3FF",
            ),
        ),
        xaxis=dict(
            gridcolor="rgba(196,181,253,0.12)",
            linecolor="rgba(196,181,253,0.22)",
            zerolinecolor="rgba(196,181,253,0.15)",
            tickfont=dict(
                color="#DDD6FE",
            ),
            title_font=dict(
                color="#DDD6FE",
            ),
        ),
        yaxis=dict(
            gridcolor="rgba(196,181,253,0.12)",
            linecolor="rgba(196,181,253,0.22)",
            zerolinecolor="rgba(196,181,253,0.15)",
            tickfont=dict(
                color="#DDD6FE",
            ),
            title_font=dict(
                color="#DDD6FE",
            ),
        ),
        hoverlabel=dict(
            bgcolor="#261B43",
            bordercolor="#8B5CF6",
            font_color="#F8F7FF",
        ),
    )

    return figura

from dashboard.conexion import probar_conexion
from dashboard.consultas import (
    obtener_total_ofertas,
    obtener_salario_promedio,
    obtener_modalidad_principal,
    obtener_ciudad_lider, 
    obtener_tecnologia_lider, 
    obtener_top_tecnologias, 
    obtener_distribucion_modalidades,
    obtener_evolucion_mensual,
    obtener_anios_disponibles,
    obtener_paises_disponibles,
    obtener_modalidades_disponibles,
    obtener_participacion_ciudades,
    obtener_salario_promedio_por_rol,
)


st.markdown(
    """
    <h1>
        Mercado Laboral
        <span style="color:#A78BFA;">
            Tecnológico
        </span>
    </h1>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Dashboard de Inteligencia de Negocios para el análisis "
    "de ofertas laborales tecnológicas."
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
    )

with col_filtro_2:
    pais_seleccionado = st.selectbox(
        "País",
        options=["Todos"] + paises_disponibles,
    )

with col_filtro_3:
    modalidad_seleccionada = st.selectbox(
        "Modalidad",
        options=["Todas"] + modalidades_disponibles,
    )

if probar_conexion():
    st.success(
        "Conexión correcta con el Data Warehouse PostgreSQL."
    )

    total_ofertas = obtener_total_ofertas()
    salario_promedio = obtener_salario_promedio()
    modalidad_principal, total_modalidad = obtener_modalidad_principal()
    ciudad_lider, total_ciudad = obtener_ciudad_lider()
    tecnologia_lider, total_tecnologia = obtener_tecnologia_lider()

    top_tecnologias = obtener_top_tecnologias(
        limite=10,
        anio=anio_seleccionado,
        pais=pais_seleccionado,
        modalidad=modalidad_seleccionada,
    )

    distribucion_modalidades = obtener_distribucion_modalidades(
        anio=anio_seleccionado,
        pais=pais_seleccionado,
    )

    participacion_ciudades = obtener_participacion_ciudades(
        anio=anio_seleccionado,
        pais=pais_seleccionado,
        modalidad=modalidad_seleccionada,
        limite=10,
    )

    salarios_por_rol = obtener_salario_promedio_por_rol(
        anio=anio_seleccionado,
        pais=pais_seleccionado,
        modalidad=modalidad_seleccionada,
    )
    
    evolucion_mensual = obtener_evolucion_mensual()

    columna_1, columna_2, columna_3, columna_4, columna_5 = st.columns(5)

    with columna_1:
        st.metric(
            label="Total de ofertas",
            value=f"{total_ofertas:,}".replace(",", "."),
            help=(
                "Cantidad total de registros almacenados "
                "en la tabla de hechos."
            ),
        )

    with columna_2:
        st.metric(
            label="Salario promedio",
            value=f"${salario_promedio:,.2f}",
            help=(
                "Promedio de los salarios registrados en la "
                "tabla de hechos, excluyendo valores nulos."
            ),
        )

    with columna_3:
        st.metric(
            label="Modalidad principal",
            value=modalidad_principal,
            delta=f"{total_modalidad} ofertas",
            help=(
                "Modalidad con mayor cantidad de ofertas "
                "registradas en el Data Warehouse."
            ),
        )
    
    with columna_4:
        st.metric(
            label="Ciudad líder",
            value=ciudad_lider,
            delta=f"{total_ciudad} ofertas",
            help=(
                "Ciudad ecuatoriana con mayor cantidad de "
                "ofertas registradas en el Data Warehouse."
            ),
        )
    
    with columna_5:
        st.metric(
            label="Tecnología líder",
            value=tecnologia_lider,
            delta=f"{total_tecnologia} ofertas",
            help=(
                "Tecnología más mencionada en las ofertas "
                "registradas en el Data Warehouse."
            ),
        )
    
    st.markdown("---")
    st.markdown("## Análisis general del mercado laboral")

    col_grafico_1, col_grafico_2 = st.columns(
        [1.4, 1],
        gap="large",
    )

    with col_grafico_1:
        st.subheader("Tecnologías más demandadas")

        if top_tecnologias.empty:
            st.warning(
                "No existen datos disponibles para mostrar "
                "las tecnologías más demandadas."
            )
        else:
            top_tecnologias = top_tecnologias.sort_values(
                by="total_menciones",
                ascending=True,
            )

            figura_tecnologias = px.bar(
                top_tecnologias,
                x="porcentaje_participacion",
                y="nombre_tecnologia",
                orientation="h",
                labels={
                    "porcentaje_participacion": "Participación (%)",
                    "nombre_tecnologia": "Tecnología",
                },
                text="porcentaje_participacion",
                custom_data=["total_menciones"],
            )

            figura_tecnologias.update_traces(
                texttemplate="%{text:.2f}%",
                textposition="outside",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Participación: %{x:.2f}%<br>"
                    "Menciones: %{customdata[0]}"
                    "<extra></extra>"
                )
            )

            figura_tecnologias.update_layout(
                height=430,
                xaxis_title="Participación sobre las ofertas filtradas (%)",
                yaxis_title=None,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#EDE9FE",
                margin=dict(
                    l=20,
                    r=50,
                    t=20,
                    b=20,
                ),
            )

            st.plotly_chart(
                figura_tecnologias,
                use_container_width=True,
            )


    with col_grafico_2:
        st.subheader("Ofertas por modalidad")

        if distribucion_modalidades.empty:
            st.warning(
                "No existen datos disponibles para mostrar "
                "la distribución por modalidad."
            )
        else:
            figura_modalidades = px.pie(
                distribucion_modalidades,
                names="modalidad",
                values="total_ofertas",
                hole=0.55,
                custom_data=[
                    "porcentaje",
                    "total_ofertas",
                ],
            )

            figura_modalidades.update_traces(
                textposition="inside",
                texttemplate="%{label}<br>%{customdata[0]:.2f}%",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Ofertas: %{value}<br>"
                    "Participación: %{customdata[0]:.2f}%"
                    "<extra></extra>"
                ),
            )

            figura_modalidades.update_layout(
                height=430,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=20,
                ),
                legend_title_text="Modalidad",
                 paper_bgcolor="rgba(0,0,0,0)",
                 plot_bgcolor="rgba(0,0,0,0)",
            )

            st.plotly_chart(
                figura_modalidades,
                use_container_width=True,
            )

            fila_modalidad_principal = distribucion_modalidades.loc[
                distribucion_modalidades["total_ofertas"].idxmax()
            ]

            modalidad_principal_grafico = str(
                fila_modalidad_principal["modalidad"]
            )

            total_modalidad_principal = int(
                fila_modalidad_principal["total_ofertas"]
            )

            porcentaje_modalidad_principal = float(
                fila_modalidad_principal["porcentaje"]
            )

            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    border-left:4px solid #8B5CF6;
                    background:rgba(139,92,246,0.08);
                    border-radius:8px;
                    margin-top:8px;
                ">
                    <b>Insight:</b><br>
                    La modalidad predominante es
                    <b>{modalidad_principal_grafico}</b>,
                    representando
                    <b>{porcentaje_modalidad_principal:.2f}%</b>
                    del total.
                </div>
                """,
                unsafe_allow_html=True,
            )


    st.markdown("---")
    st.subheader("Participación de oportunidades laborales por ciudad")

    if participacion_ciudades.empty:
        st.warning(
            "No existen datos disponibles para mostrar "
            "la participación de ofertas por ciudad."
        )
    else:
        participacion_ciudades = participacion_ciudades.sort_values(
            by="porcentaje_participacion",
            ascending=False,
        )

        figura_ciudades = px.bar(
            participacion_ciudades,
            x="ciudad",
            y="porcentaje_participacion",
            text="porcentaje_participacion",
            custom_data=["total_ofertas"],
            labels={
                "ciudad": "Ciudad",
                "porcentaje_participacion": "Participación (%)",
            },
        )

        
        figura_ciudades.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Ofertas: %{customdata[0]}<br>"
                "Participación: %{y:.2f}%"
                "<extra></extra>"
            ),
        )

        figura_ciudades.update_layout(
            height=430,
            xaxis_title="Ciudad",
            yaxis_title="Participación (%)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#EDE9FE",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=70,
            ),
        )


        st.plotly_chart(
            figura_ciudades,
            use_container_width=True,
        )

        fila_ciudad_lider = participacion_ciudades.loc[
            participacion_ciudades["total_ofertas"].idxmax()
        ]

        ciudad_lider_grafico = str(
            fila_ciudad_lider["ciudad"]
        )

        total_ciudad_lider = int(
            fila_ciudad_lider["total_ofertas"]
        )

        porcentaje_ciudad_lider = float(
            fila_ciudad_lider["porcentaje_participacion"]
        )

        st.info(
            f"La ciudad con mayor concentración de oportunidades es "
            f"**{ciudad_lider_grafico}**, con "
            f"**{total_ciudad_lider} ofertas**, equivalentes al "
            f"**{porcentaje_ciudad_lider:.2f}%** del total filtrado."
        )

    st.markdown("---")
    st.subheader("Salario promedio por categoría de rol")

    if salarios_por_rol.empty:

        st.warning(
            "No existen salarios registrados para los filtros seleccionados."
        )

    else:

        salarios_por_rol = salarios_por_rol.sort_values(
            by="salario_promedio",
            ascending=True,
        )
        figura_salarios = px.bar(
            salarios_por_rol,
            x="salario_promedio",
            y="categoria_rol",
            orientation="h",
            text="salario_promedio",
            custom_data=[
                "total_ofertas"
            ],
            labels={
                "categoria_rol": "Categoría",
                "salario_promedio": "Salario promedio (USD)",
            },
        )
        figura_salarios.update_traces(
            texttemplate="$%{text:.2f}",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Salario promedio: $%{x:.2f}<br>"
                "Ofertas analizadas: %{customdata[0]}"
                "<extra></extra>"

            ),

        )

        figura_salarios.update_layout(
            height=430,
            xaxis_title="Salario promedio (USD)",
            yaxis_title=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#EDE9FE",
            margin=dict(
                l=20,
                r=40,
                t=20,
                b=20,
            ),
            showlegend=False,
        )

        st.plotly_chart(
            figura_salarios,
            use_container_width=True,
        )

        rol_maximo = salarios_por_rol.iloc[-1]
        st.success(
            f"La categoría **{rol_maximo['categoria_rol']}** presenta "
            f"el mayor salario promedio registrado "
            f"(**${rol_maximo['salario_promedio']:.2f} USD**), "
            f"calculado sobre "
            f"**{rol_maximo['total_ofertas']} ofertas laborales**."
        )

    st.markdown("---")
    st.subheader("Evolución mensual de las ofertas laborales")

    if evolucion_mensual.empty:
        st.warning(
            "No existen datos temporales disponibles para mostrar "
            "la evolución mensual de las ofertas."
        )
    else:
        evolucion_mensual["periodo"] = (
            evolucion_mensual["periodo"].astype(str)
        )

        figura_evolucion = px.line(
            evolucion_mensual,
            x="periodo",
            y="total_ofertas",
            markers=True,
            labels={
                "periodo": "Periodo",
                "total_ofertas": "Número de ofertas",
            },
        )

        figura_evolucion.update_traces(
            mode="lines+markers",
            line={
                "width": 3,
            },
            marker={
                "size": 9,
            },
            hovertemplate=(
                "<b>Periodo: %{x}</b><br>"
                "Ofertas publicadas: %{y}"
                "<extra></extra>"
            ),
        )

        figura_evolucion.update_layout(
            height=430,
            xaxis_title="Periodo",
            yaxis_title="Número de ofertas",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#EDE9FE",
            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20,
            ),
            hovermode="x unified",
        )

        figura_evolucion.update_xaxes(
            type="category",
            tickangle=-35,
        )

        figura_evolucion.update_yaxes(
            rangemode="tozero",
            dtick=8,
        )

        st.plotly_chart(
            figura_evolucion,
            use_container_width=True,
        )

        fila_periodo_maximo = evolucion_mensual.loc[
            evolucion_mensual["total_ofertas"].idxmax()
        ]

        periodo_maximo = str(
            fila_periodo_maximo["periodo"]
        )

        ofertas_maximas = int(
            fila_periodo_maximo["total_ofertas"]
        )

        st.info(
            f"El periodo con mayor publicación de ofertas fue "
            f"**{periodo_maximo}**, con un total de "
            f"**{ofertas_maximas} ofertas laborales**."
        )

else:
    st.error(
        "No se pudo establecer conexión con PostgreSQL. "
        "Verifica que el servicio esté iniciado y que las "
        "credenciales sean correctas."
    )