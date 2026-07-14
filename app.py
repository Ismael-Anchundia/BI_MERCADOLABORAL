import streamlit as st


st.set_page_config(
    page_title="Mercado Laboral TI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


pagina_resumen = st.Page(
    "vistas/resumen.py",
    title="Resumen ejecutivo",
    icon="📊",
    default=True,
)

pagina_analisis = st.Page(
    "vistas/analisis.py",
    title="Análisis detallado",
    icon="📈",
)

navegacion = st.navigation(
    {
        "Dashboard": [
            pagina_resumen,
            pagina_analisis,
        ]
    }
)

navegacion.run()