import streamlit as st


def aplicar_estilos() -> None:
    st.markdown(
        """
        <style>
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

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }

        h1 {
            color: #f8fafc !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em;
        }

        h2, h3 {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }

        [data-testid="stCaptionContainer"] {
            color: #94a3b8 !important;
        }

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

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: linear-gradient(
                90deg,
                #6d28d9,
                #8b5cf6
            );
            border-radius: 10px;
        }

        div[data-baseweb="select"] > div {
            background-color: #2a1d49 !important;
            border: 1px solid #6d4fa3 !important;
            border-radius: 10px !important;
            color: #f8f7ff !important;
            min-height: 46px;
        }

        div[data-baseweb="select"] span {
            color: #f8f7ff !important;
        }

        label[data-testid="stWidgetLabel"] p {
            color: #f8f7ff !important;
            font-weight: 500 !important;
        }

        div[role="listbox"] {
            background-color: #261b43 !important;
            color: #f8f7ff !important;
        }

        div[role="option"] {
            color: #f8f7ff !important;
        }

        div[role="option"]:hover {
            background-color: #3b2863 !important;
        }

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

        [data-testid="stPlotlyChart"] {
            background: transparent;
            border: none;
            padding: 0;
            box-shadow: none;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid rgba(167, 139, 250, 0.22);
            border-radius: 12px;
            overflow: hidden;
        }

        [data-testid="stAlert"] {
            border-radius: 10px;
        }

        hr {
            border-color: rgba(148, 163, 184, 0.18);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def mostrar_insight(texto: str) -> None:
    st.markdown(
        f"""
        <div style="
            padding:14px 16px;
            border-left:4px solid #8B5CF6;
            background:rgba(139,92,246,0.08);
            border-radius:10px;
            margin-bottom:12px;
            line-height:1.5;
        ">
            <b>Insight:</b><br>
            {texto}
        </div>
        """,
        unsafe_allow_html=True,
    )