import io
from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="PN",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta Futurista: cyberpunk + tech
COLORS = {
    "bg_dark": "#0a0e27",      # Fondo oscuro profundo
    "bg_darker": "#050912",    # Fondo más oscuro
    "neon_cyan": "#00f0ff",    # Cian neón
    "neon_magenta": "#ff00ff", # Magenta neón
    "neon_purple": "#b000ff",  # Púrpura neón
    "neon_green": "#00ff88",   # Verde neón
    "neon_pink": "#ff0080",    # Rosa neón
    "dark_cyan": "#005f7f",    # Cyan oscuro
    "dark_magenta": "#5f0080", # Magenta oscuro
    "white": "#ffffff",
    "gray_dark": "#1a1f3a",    # Gris tech
    "gray_medium": "#2d3561",  # Gris medio tech
}

st.markdown(
    f"""
    <style>
    :root {{
        --bg-dark: {COLORS["bg_dark"]};
        --bg-darker: {COLORS["bg_darker"]};
        --neon-cyan: {COLORS["neon_cyan"]};
        --neon-magenta: {COLORS["neon_magenta"]};
        --neon-purple: {COLORS["neon_purple"]};
        --neon-green: {COLORS["neon_green"]};
        --neon-pink: {COLORS["neon_pink"]};
        --dark-cyan: {COLORS["dark_cyan"]};
        --dark-magenta: {COLORS["dark_magenta"]};
        --white: {COLORS["white"]};
        --gray-dark: {COLORS["gray_dark"]};
        --gray-medium: {COLORS["gray_medium"]};
    }}

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    html, body, [class*="css"] {{
        font-family: 'Courier New', 'Courier', monospace;
        color: var(--neon-cyan);
        background: var(--bg-dark);
        letter-spacing: 0.05em;
        line-height: 1.6;
    }}

    .stApp {{
        background: var(--bg-dark);
        background-image: 
            repeating-linear-gradient(
                0deg,
                rgba(0, 240, 255, 0.03) 0px,
                rgba(0, 240, 255, 0.03) 1px,
                transparent 1px,
                transparent 2px
            );
    }}

    /* Sidebar futurista */
    [data-testid="stSidebar"] {{
        background: var(--bg-darker);
        border-right: 2px solid var(--neon-cyan);
        box-shadow: -10px 0 40px rgba(0, 240, 255, 0.2);
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        padding: 1.5rem 1rem;
    }}

    /* Header principal futurista */
    .main-title {{
        background: linear-gradient(135deg, var(--bg-darker) 0%, rgba(0, 240, 255, 0.1) 100%);
        color: var(--neon-cyan);
        padding: 3rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        letter-spacing: 0.1em;
        border-bottom: 3px solid var(--neon_magenta);
        border-top: 3px solid var(--neon-cyan);
        box-shadow: 
            0 0 20px rgba(0, 240, 255, 0.3),
            inset 0 0 20px rgba(0, 240, 255, 0.05);
        position: relative;
    }}

    .main-title::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    }}

    .main-title h1 {{
        margin: 0;
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.5), 0 0 40px rgba(255, 0, 255, 0.3);
        text-transform: uppercase;
    }}

    .main-title p {{
        margin: 0.8rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
        font-weight: 400;
        letter-spacing: 0.05em;
        color: var(--neon-green);
    }}

    /* Tarjetas futuristas */
    .card {{
        background: linear-gradient(135deg, rgba(26, 31, 58, 0.5) 0%, rgba(45, 53, 97, 0.3) 100%);
        border: 2px solid var(--neon-cyan);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 
            0 0 20px rgba(0, 240, 255, 0.2),
            inset 0 0 20px rgba(0, 240, 255, 0.05);
        position: relative;
        overflow: hidden;
    }}

    .card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
        animation: scan 8s linear infinite;
    }}

    .card:hover {{
        border-color: var(--neon_magenta);
        box-shadow: 
            0 0 40px rgba(255, 0, 255, 0.4),
            inset 0 0 20px rgba(255, 0, 255, 0.1);
        transition: all 0.3s ease;
    }}

    @keyframes scan {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
    }}

    /* Etiquetas de sección */
    .section-label {{
        color: var(--neon_magenta);
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        margin-top: 2rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        border-bottom: 2px solid var(--neon-cyan);
        border-top: 1px solid rgba(0, 240, 255, 0.3);
        padding: 0.8rem 0;
        display: inline-block;
        text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
        position: relative;
    }}

    .section-label::after {{
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--neon-cyan), var(--neon_magenta), var(--neon_purple));
        animation: shimmer 3s linear infinite;
    }}

    @keyframes shimmer {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}

    /* Mini tarjetas para métricas */
    .mini-card {{
        background: linear-gradient(135deg, rgba(26, 31, 58, 0.6) 0%, rgba(45, 53, 97, 0.4) 100%);
        border: 2px solid var(--dark-cyan);
        padding: 1.2rem;
        margin-bottom: 1rem;
        min-height: 110px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}

    .mini-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at top right, rgba(0, 240, 255, 0.1), transparent);
        pointer-events: none;
    }}

    .mini-card:hover {{
        border-color: var(--neon-cyan);
        box-shadow: 
            0 0 30px rgba(0, 240, 255, 0.3),
            inset 0 0 20px rgba(0, 240, 255, 0.1);
    }}

    .mini-card .kicker {{
        color: var(--neon-green);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.6rem;
    }}

    .mini-card .value {{
        color: var(--neon-cyan);
        font-size: 1.6rem;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 0.3rem;
        word-break: break-word;
        letter-spacing: -0.02em;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }}

    .mini-card .sub {{
        color: rgba(0, 240, 255, 0.7);
        font-size: 0.85rem;
        font-weight: 400;
    }}

    /* Métricas de Streamlit */
    div[data-testid="stMetric"] {{
        background: linear-gradient(135deg, rgba(26, 31, 58, 0.5) 0%, rgba(45, 53, 97, 0.3) 100%);
        border: 2px solid var(--neon-cyan);
        padding: 1.2rem;
        border-radius: 0;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    }}

    /* Nota informativa */
    .note {{
        font-size: 0.95rem;
        color: var(--neon-green);
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.05) 0%, rgba(0, 240, 255, 0.05) 100%);
        padding: 1rem 1.2rem;
        border-left: 4px solid var(--neon-green);
        border-right: 1px solid rgba(0, 255, 136, 0.3);
        margin: 1.5rem 0;
        font-weight: 500;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.1);
    }}

    /* Badges */
    .ok-badge {{
        display: inline-block;
        background: rgba(0, 255, 136, 0.15);
        color: var(--neon-green);
        padding: 0.35rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        border: 1px solid rgba(0, 255, 136, 0.4);
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.3), inset 0 0 10px rgba(0, 255, 136, 0.1);
    }}

    .warn-badge {{
        display: inline-block;
        background: rgba(255, 0, 128, 0.15);
        color: var(--neon-pink);
        padding: 0.35rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        border: 1px solid rgba(255, 0, 128, 0.4);
        box-shadow: 0 0 10px rgba(255, 0, 128, 0.3), inset 0 0 10px rgba(255, 0, 128, 0.1);
    }}

    .small {{
        font-size: 0.85rem;
        color: rgba(0, 240, 255, 0.7);
        font-weight: 400;
    }}

    /* Tarjetas delta */
    .delta-card {{
        background: linear-gradient(135deg, rgba(26, 31, 58, 0.6) 0%, rgba(45, 53, 97, 0.4) 100%);
        border: 2px solid var(--neon-purple);
        padding: 1.2rem;
        margin-bottom: 1rem;
        min-height: 135px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}

    .delta-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at center, rgba(176, 0, 255, 0.1), transparent);
        pointer-events: none;
    }}

    .delta-card:hover {{
        border-color: var(--neon_magenta);
        box-shadow: 
            0 0 30px rgba(255, 0, 255, 0.3),
            inset 0 0 20px rgba(255, 0, 255, 0.1);
    }}

    .delta-card .kicker {{
        color: var(--neon-green);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.6rem;
    }}

    .delta-card .value {{
        color: var(--neon-cyan);
        font-size: 1.5rem;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 0.5rem;
        word-break: break-word;
        letter-spacing: -0.02em;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }}

    .delta-pill {{
        display: inline-block;
        padding: 0.35rem 0.8rem;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        border: 1px solid transparent;
    }}

    .delta-positive {{
        background: rgba(0, 255, 136, 0.2);
        color: var(--neon-green);
        border-color: rgba(0, 255, 136, 0.4);
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
    }}

    .delta-warning {{
        background: rgba(255, 193, 7, 0.2);
        color: #ffc107;
        border-color: rgba(255, 193, 7, 0.4);
        box-shadow: 0 0 10px rgba(255, 193, 7, 0.3);
    }}

    .delta-negative {{
        background: rgba(255, 0, 128, 0.2);
        color: var(--neon-pink);
        border-color: rgba(255, 0, 128, 0.4);
        box-shadow: 0 0 10px rgba(255, 0, 128, 0.3);
    }}

    .delta-neutral {{
        background: rgba(0, 240, 255, 0.1);
        color: var(--neon-cyan);
        border-color: rgba(0, 240, 255, 0.3);
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }}

    .delta-card .sub {{
        color: rgba(0, 240, 255, 0.7);
        font-size: 0.8rem;
        font-weight: 400;
    }}

    /* Tabs */
    [data-baseweb="tab"] {{
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-size: 0.85rem;
        color: var(--neon-cyan);
    }}

    /* Selectores y filtros */
    [data-baseweb="select"] {{
        font-size: 0.9rem;
    }}

    input[type="text"],
    input[type="number"],
    select {{
        border: 2px solid var(--neon-cyan) !important;
        background: var(--bg-darker) !important;
        color: var(--neon-cyan) !important;
        font-size: 0.9rem;
        font-family: 'Courier New', monospace;
        padding: 0.6rem !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2) !important;
    }}

    input[type="text"]::placeholder,
    input[type="number"]::placeholder {{
        color: rgba(0, 240, 255, 0.5) !important;
    }}

    input[type="text"]:focus,
    input[type="number"]:focus,
    select:focus {{
        border-color: var(--neon_magenta) !important;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.4) !important;
    }}

    /* Botones */
    .stButton > button {{
        background: linear-gradient(135deg, var(--dark-cyan) 0%, var(--dark-magenta) 100%);
        color: var(--neon-cyan);
        border: 2px solid var(--neon-cyan);
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-size: 0.85rem;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
    }}

    .stButton > button:hover {{
        background: linear-gradient(135deg, var(--dark-magenta) 0%, var(--dark-cyan) 100%);
        border-color: var(--neon_magenta);
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.5);
    }}

    /* DataFrames */
    [data-testid="stDataFrame"] {{
        font-size: 0.9rem;
    }}

    .stDataFrame {{
        background: linear-gradient(135deg, rgba(26, 31, 58, 0.5) 0%, rgba(45, 53, 97, 0.3) 100%);
    }}

    /* Expanders */
    [data-testid="stExpander"] {{
        border: 2px solid var(--neon-cyan);
        background: rgba(26, 31, 58, 0.5);
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    }}

    /* Info y Warning */
    [data-testid="stAlert"] {{
        padding: 1rem;
        border-radius: 0;
        border-left: 4px solid var(--neon-cyan);
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.1) 0%, rgba(0, 240, 255, 0.05) 100%);
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    }}

    /* Scrollbar futurista */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}

    ::-webkit-scrollbar-track {{
        background: var(--bg-darker);
    }}

    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, var(--neon-cyan), var(--neon_magenta));
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, var(--neon_magenta), var(--neon-cyan));
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
    }}

    /* Líneas de escaneo animadas */
    @keyframes flicker {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}

    /* Efecto glow en texto */
    .stMarkdown {{
        color: var(--neon-cyan);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

REQUIRED_COLUMNS = [
    "PERIODO_MES",
    "ACUERDO_VENTAS",
    "ACUERDO_IMMG",
    "CONTRATO",
    "INQUILINO",
    "NOMENCLATURA",
    "LOCAL",
    "TASA_VENTAS",
    "VENTA_REPORTADA",
    "ALQUILER_VAR_VENTAS",
    "TASA_PASAJEROS",
    "PASAJEROS",
    "ALQUILER_VAR_PASAJEROS",
    "FACTURADO_VARIABLE",
]


def format_currency(value: float) -> str:
    return f"${value:,.0f}".replace(",", ".")


def format_number(value: float) -> str:
    return f"{value:,.0f}".replace(",", ".")


FORMAT_MAP = {
    "TOTAL_COBRO_CALCULADO": "currency",
    "CICLO_1_PASAJEROS": "currency",
    "CICLO_2_VENTAS": "currency",
    "ALQUILER_VAR_PASAJEROS": "currency",
    "ALQUILER_VAR_VENTAS": "currency",
    "FACTURADO_VARIABLE": "currency",
    "VENTA_REPORTADA": "currency",
    "PASAJEROS": "number",
}


def format_metric_value(value: float, metric: str) -> str:
    if FORMAT_MAP.get(metric) == "currency":
        return format_currency(value)
    return format_number(value)


def format_metric_delta(value: float, metric: str) -> str:
    if FORMAT_MAP.get(metric) == "currency":
        return format_currency(value)
    return ("-" if value < 0 else "") + format_number(abs(value))


def validate_columns(df: pd.DataFrame) -> List[str]:
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


@st.cache_data(show_spinner=False)
def load_data(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df.columns = [str(c).strip().upper() for c in df.columns]

    missing = validate_columns(df)
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {', '.join(missing)}")

    df["PERIODO_MES"] = pd.to_datetime(df["PERIODO_MES"].astype(str), format="%Y-%m", errors="coerce")
    if df["PERIODO_MES"].isna().any():
        raise ValueError("La columna PERIODO_MES debe venir en formato YYYY-MM.")

    numeric_cols = [
        "ACUERDO_VENTAS",
        "ACUERDO_IMMG",
        "TASA_VENTAS",
        "VENTA_REPORTADA",
        "ALQUILER_VAR_VENTAS",
        "TASA_PASAJEROS",
        "PASAJEROS",
        "ALQUILER_VAR_PASAJEROS",
        "FACTURADO_VARIABLE",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    text_cols = ["CONTRATO", "INQUILINO", "NOMENCLATURA", "LOCAL"]
    for col in text_cols:
        df[col] = df[col].astype(str).fillna("").str.strip()

    df["CICLO_1_PASAJEROS"] = df["ALQUILER_VAR_PASAJEROS"].clip(lower=0)
    df["CICLO_2_VENTAS"] = (df["ALQUILER_VAR_VENTAS"] - df["ALQUILER_VAR_PASAJEROS"]).clip(lower=0)
    df["TOTAL_COBRO_CALCULADO"] = df["CICLO_1_PASAJEROS"] + df["CICLO_2_VENTAS"]
    df["TOTAL_COBRO_MAXIMO"] = df[["ALQUILER_VAR_PASAJEROS", "ALQUILER_VAR_VENTAS"]].max(axis=1)
    df["DIF_VENTAS_VS_PASAJEROS"] = df["ALQUILER_VAR_VENTAS"] - df["ALQUILER_VAR_PASAJEROS"]
    df["VENTAS_SUPERA_PASAJEROS"] = df["ALQUILER_VAR_VENTAS"] > df["ALQUILER_VAR_PASAJEROS"]

    df["VALIDA_ALQ_VENTAS"] = np.isclose(
        df["ALQUILER_VAR_VENTAS"],
        df["TASA_VENTAS"] * df["VENTA_REPORTADA"],
        rtol=1e-05,
        atol=1,
    )
    df["VALIDA_ALQ_PASAJEROS"] = np.isclose(
        df["ALQUILER_VAR_PASAJEROS"],
        df["TASA_PASAJEROS"] * df["PASAJEROS"],
        rtol=1e-05,
        atol=1,
    )
    df["VALIDA_FACTURADO_VARIABLE"] = np.isclose(
        df["FACTURADO_VARIABLE"],
        df["ALQUILER_VAR_VENTAS"] - df["ALQUILER_VAR_PASAJEROS"],
        rtol=1e-05,
        atol=1,
    )
    df["VALIDA_TOTAL_COBRO"] = np.isclose(
        df["TOTAL_COBRO_CALCULADO"],
        df["TOTAL_COBRO_MAXIMO"],
        rtol=1e-05,
        atol=1,
    )

    meses_es = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
        7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    df["PERIODO_NUM_MES"] = df["PERIODO_MES"].dt.month
    df["PERIODO_ANIO"] = df["PERIODO_MES"].dt.year
    df["MES_NOMBRE"] = df["PERIODO_NUM_MES"].map(meses_es)
    df["PERIODO_LABEL"] = df["MES_NOMBRE"] + " " + df["PERIODO_ANIO"].astype(str)
    return df


def build_download(df: pd.DataFrame) -> bytes:
    export_cols = [
        "PERIODO_LABEL",
        "CONTRATO",
        "INQUILINO",
        "NOMENCLATURA",
        "LOCAL",
        "ACUERDO_VENTAS",
        "ACUERDO_IMMG",
        "TASA_VENTAS",
        "VENTA_REPORTADA",
        "ALQUILER_VAR_VENTAS",
        "TASA_PASAJEROS",
        "PASAJEROS",
        "ALQUILER_VAR_PASAJEROS",
        "FACTURADO_VARIABLE",
        "CICLO_1_PASAJEROS",
        "CICLO_2_VENTAS",
        "TOTAL_COBRO_CALCULADO",
        "VALIDA_ALQ_VENTAS",
        "VALIDA_ALQ_PASAJEROS",
        "VALIDA_FACTURADO_VARIABLE",
        "VALIDA_TOTAL_COBRO",
    ]
    output = io.StringIO()
    df[export_cols].to_csv(output, index=False)
    return output.getvalue().encode("utf-8")


def style_plot(fig):
    fig.update_layout(
        paper_bgcolor=COLORS["bg_dark"],
        plot_bgcolor="rgba(5, 9, 18, 0.5)",
        font=dict(family="'Courier New', 'Courier', monospace", color=COLORS["neon_cyan"], size=10),
        legend_title_text="",
        margin=dict(l=50, r=20, t=60, b=50),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, linecolor=COLORS["neon_cyan"], linewidth=1.5, zeroline=False)
    fig.update_yaxes(gridcolor=f"rgba(0, 240, 255, 0.1)", linecolor=COLORS["neon_cyan"], linewidth=1.5, zeroline=False)
    
    # Renombrar trazas y asignar colores
    for trace in getattr(fig, "data", []):
        if getattr(trace, "name", None) == "CICLO_1_PASAJEROS":
            trace.name = "Ciclo 2"
            trace.marker.color = COLORS["neon_cyan"]
        elif getattr(trace, "name", None) == "CICLO_2_VENTAS":
            trace.name = "Ciclo 3"
            trace.marker.color = COLORS["neon_magenta"]
        elif getattr(trace, "name", None) == "ALQUILER_VAR_PASAJEROS":
            trace.name = "Cobro por pasajeros"
            trace.line.color = COLORS["neon_cyan"]
        elif getattr(trace, "name", None) == "ALQUILER_VAR_VENTAS":
            trace.name = "Cobro por ventas"
            trace.line.color = COLORS["neon_magenta"]
        elif getattr(trace, "name", None) == "TOTAL_COBRO_CALCULADO":
            trace.name = "Total cobrado"
            trace.line.color = COLORS["neon_green"]
    
    return fig


def render_info_card(title: str, value: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="mini-card">
            <div class="kicker">{title}</div>
            <div class="value">{value}</div>
            <div class="sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def classify_variation(delta_pct: float) -> tuple[str, str, str]:
    if pd.isna(delta_pct):
        return "Sin base comparable", "delta-neutral", "–"
    if delta_pct >= 0:
        return "Crecimiento", "delta-positive", "↑"
    if delta_pct > -10:
        return "Caída leve", "delta-warning", "↓"
    return "Caída fuerte", "delta-negative", "↓↓"


def render_variation_card(title: str, value: str, badge_text: str, badge_class: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="delta-card">
            <div class="kicker">{title}</div>
            <div class="value">{value}</div>
            <div class="delta-pill {badge_class}">{badge_text}</div>
            <div class="sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_month_filter(data: pd.DataFrame, label: str, key: str) -> pd.DataFrame:
    month_options = (
        data[["PERIODO_MES", "PERIODO_LABEL"]]
        .drop_duplicates()
        .sort_values("PERIODO_MES")["PERIODO_LABEL"]
        .tolist()
    )

    if not month_options:
        return data.iloc[0:0].copy()

    selected_months = st.multiselect(
        label,
        options=month_options,
        default=month_options,
        key=key,
    )

    if not selected_months:
        return data.iloc[0:0].copy()

    return data[data["PERIODO_LABEL"].isin(selected_months)].copy()


def render_same_month_comparison(data: pd.DataFrame, section_key: str, title: str) -> pd.DataFrame:
    st.markdown(f'<div class="section-label">{title}</div>', unsafe_allow_html=True)

    if data.empty:
        st.info("No hay datos disponibles para comparar.")
        return data.iloc[0:0].copy()

    month_order = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    month_options = [m for m in month_order if m in data["MES_NOMBRE"].dropna().unique().tolist()]
    year_options = sorted(data["PERIODO_ANIO"].dropna().astype(int).unique().tolist())

    c1, c2 = st.columns([1, 1.3])
    with c1:
        selected_month_name = st.selectbox(
            "Mes a comparar",
            options=month_options,
            key=f"{section_key}_compare_month",
        )
    with c2:
        default_years = year_options[-2:] if len(year_options) >= 2 else year_options
        selected_years = st.multiselect(
            "Años a comparar",
            options=year_options,
            default=default_years,
            key=f"{section_key}_compare_years",
        )

    if not selected_month_name or not selected_years:
        st.info("Selecciona al menos un mes y un año para habilitar la comparación.")
        return data.iloc[0:0].copy()

    compare_df = data[
        (data["MES_NOMBRE"] == selected_month_name)
        & (data["PERIODO_ANIO"].isin(selected_years))
    ].copy()

    if compare_df.empty:
        st.warning("No hay registros para la combinación de mes y años seleccionada.")
        return compare_df

    compare_df["ANIO_LABEL"] = compare_df["PERIODO_ANIO"].astype(str)
    return compare_df


def compute_variation_summary(compare_summary: pd.DataFrame, metrics: List[str]) -> pd.DataFrame:
    if compare_summary.empty or "PERIODO_ANIO" not in compare_summary.columns:
        return pd.DataFrame()

    ordered = compare_summary.sort_values("PERIODO_ANIO").reset_index(drop=True).copy()
    if len(ordered) < 2:
        return pd.DataFrame()

    previous_row = ordered.iloc[-2]
    current_row = ordered.iloc[-1]

    results = []
    for metric in metrics:
        previous_value = float(previous_row.get(metric, 0))
        current_value = float(current_row.get(metric, 0))
        absolute_change = current_value - previous_value
        pct_change = (absolute_change / previous_value * 100) if previous_value != 0 else np.nan
        results.append(
            {
                "Indicador": metric,
                "Año base": int(previous_row["PERIODO_ANIO"]),
                "Año comparado": int(current_row["PERIODO_ANIO"]),
                "Valor base": previous_value,
                "Valor comparado": current_value,
                "Variación absoluta": absolute_change,
                "Variación %": pct_change,
            }
        )

    return pd.DataFrame(results)


def render_variation_cards(variation_df: pd.DataFrame, labels_map: dict, section_title: str):
    st.markdown(f'<div class="section-label">{section_title}</div>', unsafe_allow_html=True)

    if variation_df.empty:
        st.info("Se requieren al menos dos años para calcular la variación frente al periodo anterior.")
        return

    metric_cols = st.columns(len(variation_df))
    for idx, (_, row) in enumerate(variation_df.iterrows()):
        label = labels_map.get(row["Indicador"], row["Indicador"])
        delta_abs = row["Variación absoluta"]
        delta_pct = row["Variación %"]
        status_text, badge_class, arrow = classify_variation(delta_pct)

        pct_text = "Sin base comparable" if pd.isna(delta_pct) else f"{arrow} {delta_pct:+.1f}%"
        badge_text = status_text if pd.isna(delta_pct) else f"{status_text} | {pct_text}"
        subtitle = (
            f"{int(row['Año comparado'])} vs {int(row['Año base'])} | Variación absoluta: {format_metric_delta(delta_abs, row['Indicador'])}"
            if not pd.isna(delta_pct)
            else f"{int(row['Año comparado'])} vs {int(row['Año base'])} | base del año anterior en cero"
        )
        with metric_cols[idx]:
            render_variation_card(
                label,
                format_metric_value(row["Valor comparado"], row["Indicador"]),
                badge_text,
                badge_class,
                subtitle,
            )


def build_variation_display_table(variation_df: pd.DataFrame, labels_map: dict) -> pd.DataFrame:
    if variation_df.empty:
        return variation_df

    display = variation_df.copy()
    display["Semáforo"] = display["Variación %"].map(lambda x: classify_variation(x)[0])
    display["Indicador"] = display["Indicador"].map(lambda x: labels_map.get(x, x))
    display["Valor base"] = display.apply(lambda row: format_metric_value(row["Valor base"], row["Indicador"]), axis=1)
    display["Valor comparado"] = display.apply(lambda row: format_metric_value(row["Valor comparado"], row["Indicador"]), axis=1)
    display["Variación absoluta"] = display.apply(lambda row: format_metric_delta(row["Variación absoluta"], row["Indicador"]), axis=1)
    display["Variación %"] = display["Variación %"].map(
        lambda x: "Sin base comparable" if pd.isna(x) else f"{x:+.1f}%"
    )
    return display[[
        "Indicador",
        "Año base",
        "Año comparado",
        "Valor base",
        "Valor comparado",
        "Variación absoluta",
        "Variación %",
        "Semáforo",
    ]]


def create_year_bridge_chart(compare_summary: pd.DataFrame) -> go.Figure:
    ordered = compare_summary.sort_values("PERIODO_ANIO").reset_index(drop=True)
    if len(ordered) < 2:
        return go.Figure()

    base_year = int(ordered.iloc[-2]["PERIODO_ANIO"])
    compare_year = int(ordered.iloc[-1]["PERIODO_ANIO"])

    base_total = float(ordered.iloc[-2]["TOTAL_COBRO_CALCULADO"])
    delta_pasajeros = float(ordered.iloc[-1]["ALQUILER_VAR_PASAJEROS"] - ordered.iloc[-2]["ALQUILER_VAR_PASAJEROS"])
    delta_ventas = float(ordered.iloc[-1]["ALQUILER_VAR_VENTAS"] - ordered.iloc[-2]["ALQUILER_VAR_VENTAS"])
    final_total = float(ordered.iloc[-1]["TOTAL_COBRO_CALCULADO"])

    fig = go.Figure(
        go.Waterfall(
            name="Puente de valor",
            orientation="v",
            measure=["absolute", "relative", "relative", "total"],
            x=[
                f"Total {base_year}",
                "Δ cobro pasajeros",
                "Δ cobro ventas",
                f"Total {compare_year}",
            ],
            y=[base_total, delta_pasajeros, delta_ventas, final_total],
            text=[
                format_currency(base_total),
                format_metric_delta(delta_pasajeros, "ALQUILER_VAR_PASAJEROS"),
                format_metric_delta(delta_ventas, "ALQUILER_VAR_VENTAS"),
                format_currency(final_total),
            ],
            textposition="outside",
            connector={"line": {"color": "rgba(255,255,255,0.25)", "width": 1}},
            increasing={"marker": {"color": COLORS["neon_green"]}},
            decreasing={"marker": {"color": COLORS["neon_pink"]}},
            totals={"marker": {"color": COLORS["neon_cyan"]}},
        )
    )
    fig.update_layout(
        title=f"Puente de valor: {base_year} vs {compare_year}",
        showlegend=False,
        yaxis_title="Valor",
    )
    return fig


def build_year_comparison_narrative(compare_summary: pd.DataFrame) -> str:
    ordered = compare_summary.sort_values("PERIODO_ANIO").reset_index(drop=True)
    if len(ordered) < 2:
        return ""

    base_year = int(ordered.iloc[-2]["PERIODO_ANIO"])
    compare_year = int(ordered.iloc[-1]["PERIODO_ANIO"])

    delta_total = float(ordered.iloc[-1]["TOTAL_COBRO_CALCULADO"] - ordered.iloc[-2]["TOTAL_COBRO_CALCULADO"])
    delta_pasajeros = float(ordered.iloc[-1]["ALQUILER_VAR_PASAJEROS"] - ordered.iloc[-2]["ALQUILER_VAR_PASAJEROS"])
    delta_ventas = float(ordered.iloc[-1]["ALQUILER_VAR_VENTAS"] - ordered.iloc[-2]["ALQUILER_VAR_VENTAS"])

    tendencia_total = "creció" if delta_total > 0 else "cayó" if delta_total < 0 else "se mantuvo estable"
    impacto_principal = "cobro por ventas" if abs(delta_ventas) >= abs(delta_pasajeros) else "cobro por pasajeros"
    direccion_principal = delta_ventas if abs(delta_ventas) >= abs(delta_pasajeros) else delta_pasajeros
    verbo_principal = "aumentó" if direccion_principal > 0 else "disminuyó" if direccion_principal < 0 else "se mantuvo estable"

    return (
        f"Entre {base_year} y {compare_year}, el total cobrado {tendencia_total} "
        f"en {format_currency(abs(delta_total)) if delta_total != 0 else format_currency(0)}. "
        f"El mayor efecto vino del {impacto_principal}, que {verbo_principal}."
    )


# Header principal
st.markdown(
    """
    <div class="main-title">
        <h1>Dashboard de Cobro Variable</h1>
        <p>Visualización de ciclo 2 (pasajeros) y ciclo 3 (ventas) con validación de acuerdos y comportamiento mensual.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("📘 Lógica de negocio aplicada", expanded=False):
    st.markdown(
        """
        - **Ciclo 2:** se cobra siempre el valor de **ALQUILER_VAR_PASAJEROS**.
        - **Ciclo 3:** solo se cobra cuando **ALQUILER_VAR_VENTAS > ALQUILER_VAR_PASAJEROS**.
        - **Valor adicional ciclo 3:** `ALQUILER_VAR_VENTAS - ALQUILER_VAR_PASAJEROS`.
        - **Total cobrado al inquilino:** `máximo(ALQUILER_VAR_VENTAS, ALQUILER_VAR_PASAJEROS)`.
        """
    )

st.sidebar.header("Carga y filtros")
uploaded_file = st.sidebar.file_uploader("Sube el archivo CSV", type=["csv"])

st.sidebar.markdown(
    """
    <div class="small">
    Tipografía del sistema: -apple-system, BlinkMacSystemFont, Segoe UI.<br>
    Estilos premium inspirados en Genesis.
    </div>
    """,
    unsafe_allow_html=True,
)

if uploaded_file is None:
    st.info("Carga un archivo CSV con la estructura indicada para habilitar el dashboard.")
    st.stop()

try:
    df = load_data(uploaded_file)
except Exception as e:
    st.error(f"No fue posible procesar el archivo: {e}")
    st.stop()

periodos = (
    df[["PERIODO_MES", "PERIODO_LABEL"]]
    .drop_duplicates()
    .sort_values("PERIODO_MES")["PERIODO_LABEL"]
    .tolist()
)
inquilinos = sorted(df["INQUILINO"].dropna().unique().tolist())
locales = sorted(df["LOCAL"].dropna().unique().tolist())
nomenclaturas = sorted(df["NOMENCLATURA"].dropna().unique().tolist())

selected_periodos = st.sidebar.multiselect("Periodo mes", options=periodos, default=periodos)
selected_inquilinos = st.sidebar.multiselect("Inquilino", options=inquilinos, default=inquilinos)
selected_locales = st.sidebar.multiselect("Local", options=locales, default=locales)
selected_nomenclaturas = st.sidebar.multiselect("Nomenclatura", options=nomenclaturas, default=nomenclaturas)

filtered = df[
    df["PERIODO_LABEL"].isin(selected_periodos)
    & df["INQUILINO"].isin(selected_inquilinos)
    & df["LOCAL"].isin(selected_locales)
    & df["NOMENCLATURA"].isin(selected_nomenclaturas)
].copy()

if filtered.empty:
    st.warning("No hay datos con los filtros seleccionados.")
    st.stop()

total_ciclo_2 = filtered["CICLO_1_PASAJEROS"].sum()
total_ciclo_3 = filtered["CICLO_2_VENTAS"].sum()
total_cobrado = filtered["TOTAL_COBRO_CALCULADO"].sum()
inquilinos_count = filtered["INQUILINO"].nunique()
contratos_count = filtered["CONTRATO"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Cobro ciclo 2", format_currency(total_ciclo_2))
col2.metric("Cobro ciclo 3", format_currency(total_ciclo_3))
col3.metric("Total cobrado", format_currency(total_cobrado))
col4.metric("Inquilinos", format_number(inquilinos_count))
col5.metric("Contratos", format_number(contratos_count))

st.markdown(
    """
    <div class="note">
        El total cobrado se interpreta como el mayor valor entre <b>ALQUILER_VAR_PASAJEROS</b> y <b>ALQUILER_VAR_VENTAS</b>.
        En términos operativos: <b>ciclo 2</b> asegura el mínimo por pasajeros y <b>ciclo 3</b> recauda el excedente cuando el componente por ventas es superior.
    </div>
    """,
    unsafe_allow_html=True,
)

monthly = (
    filtered.groupby(["PERIODO_MES", "PERIODO_LABEL"], as_index=False)[
        ["CICLO_1_PASAJEROS", "CICLO_2_VENTAS", "TOTAL_COBRO_CALCULADO", "ALQUILER_VAR_VENTAS", "ALQUILER_VAR_PASAJEROS"]
    ]
    .sum()
    .sort_values("PERIODO_MES")
)

top_inquilinos = (
    filtered.groupby(["INQUILINO", "ACUERDO_VENTAS", "ACUERDO_IMMG"], dropna=False, as_index=False)[
        ["CICLO_1_PASAJEROS", "CICLO_2_VENTAS", "TOTAL_COBRO_CALCULADO", "ALQUILER_VAR_VENTAS", "ALQUILER_VAR_PASAJEROS"]
    ]
    .sum()
    .sort_values("TOTAL_COBRO_CALCULADO", ascending=False)
)

cliente_options = sorted(filtered["INQUILINO"].dropna().unique().tolist())
default_cliente = cliente_options[0] if cliente_options else None
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Resumen general",
    "Estadísticas por cliente",
    "Consolidado por inquilino",
    "Validaciones",
    "Detalle",
])

with tab1:
    st.markdown('<div class="section-label">Filtro mensual del resumen</div>', unsafe_allow_html=True)
    tab1_filtered = render_month_filter(filtered, "Meses a visualizar en resumen general", "tab1_months")

    if tab1_filtered.empty:
        st.warning("No hay datos para los meses seleccionados en esta sección.")
    else:
        monthly_tab1 = (
            tab1_filtered.groupby(["PERIODO_MES", "PERIODO_LABEL"], as_index=False)[
                ["CICLO_1_PASAJEROS", "CICLO_2_VENTAS", "TOTAL_COBRO_CALCULADO", "ALQUILER_VAR_VENTAS", "ALQUILER_VAR_PASAJEROS"]
            ]
            .sum()
            .sort_values("PERIODO_MES")
        )

        c1, c2 = st.columns([1.25, 1])
        with c1:
            bar_df = monthly_tab1.melt(
                id_vars="PERIODO_LABEL",
                value_vars=["CICLO_1_PASAJEROS", "CICLO_2_VENTAS"],
                var_name="COMPONENTE",
                value_name="VALOR",
            )
            bar_df["COMPONENTE"] = bar_df["COMPONENTE"].replace(
                {"CICLO_1_PASAJEROS": "Ciclo 2 - Pasajeros", "CICLO_2_VENTAS": "Ciclo 3 - Ventas"}
            )
            fig = px.bar(
                bar_df,
                x="PERIODO_LABEL",
                y="VALOR",
                color="COMPONENTE",
                barmode="stack",
                title="Cobro mensual por componente",
                labels={"PERIODO_LABEL": "Periodo", "VALOR": "Valor", "COMPONENTE": "Componente"},
                color_discrete_map={
                    "Ciclo 2 - Pasajeros": COLORS["neon_cyan"],
                    "Ciclo 3 - Ventas": COLORS["neon_magenta"],
                },
            )
            st.plotly_chart(style_plot(fig), use_container_width=True)

        with c2:
            fig2 = px.line(
                monthly_tab1,
                x="PERIODO_LABEL",
                y=["ALQUILER_VAR_PASAJEROS", "ALQUILER_VAR_VENTAS", "TOTAL_COBRO_CALCULADO"],
                markers=True,
                title="Comparativo mensual: base pasajeros vs ventas vs cobro final",
                labels={"PERIODO_LABEL": "Periodo", "value": "Valor", "variable": "Componente"},
                color_discrete_map={
                    "ALQUILER_VAR_PASAJEROS": COLORS["gray_medium"],
                    "ALQUILER_VAR_VENTAS": COLORS["neon_magenta"],
                    "TOTAL_COBRO_CALCULADO": COLORS["neon_green"],
                },
            )
            st.plotly_chart(style_plot(fig2), use_container_width=True)

        compare_tab1 = render_same_month_comparison(
            tab1_filtered,
            "tab1",
            "Comparativa del mismo mes entre años"
        )

        if not compare_tab1.empty:
            compare_summary_tab1 = (
                compare_tab1.groupby(["PERIODO_ANIO", "ANIO_LABEL"], as_index=False)[
                    ["CICLO_1_PASAJEROS", "CICLO_2_VENTAS", "TOTAL_COBRO_CALCULADO", "ALQUILER_VAR_PASAJEROS", "ALQUILER_VAR_VENTAS"]
                ]
                .sum()
                .sort_values("PERIODO_ANIO")
            )

            g1, g2 = st.columns([1.1, 1])
            with g1:
                compare_melt = compare_summary_tab1.melt(
                    id_vars="ANIO_LABEL",
                    value_vars=["CICLO_1_PASAJEROS", "CICLO_2_VENTAS", "TOTAL_COBRO_CALCULADO"],
                    var_name="COMPONENTE",
                    value_name="VALOR",
                )
                compare_melt["COMPONENTE"] = compare_melt["COMPONENTE"].replace(
                    {
                        "CICLO_1_PASAJEROS": "Ciclo 2",
                        "CICLO_2_VENTAS": "Ciclo 3",
                        "TOTAL_COBRO_CALCULADO": "Total cobrado",
                    }
                )
                fig_compare_1 = px.bar(
                    compare_melt,
                    x="ANIO_LABEL",
                    y="VALOR",
                    color="COMPONENTE",
                    barmode="group",
                    title="Comparativo por año del mismo mes seleccionado",
                    labels={"ANIO_LABEL": "Año", "VALOR": "Valor", "COMPONENTE": "Componente"},
                    color_discrete_map={
                        "Ciclo 2": COLORS["neon_cyan"],
                        "Ciclo 3": COLORS["neon_magenta"],
                        "Total cobrado": COLORS["neon_green"],
                    },
                )
                st.plotly_chart(style_plot(fig_compare_1), use_container_width=True)

            with g2:
                fig_compare_2 = create_year_bridge_chart(compare_summary_tab1)
                st.plotly_chart(style_plot(fig_compare_2), use_container_width=True)

            narrative_text = build_year_comparison_narrative(compare_summary_tab1)
            if narrative_text:
                st.markdown(
                    f"""
                    <div class="note">
                        <b>Lectura ejecutiva:</b> {narrative_text}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            compare_labels_tab1 = {
                "CICLO_1_PASAJEROS": "Ciclo 2",
                "CICLO_2_VENTAS": "Ciclo 3",
                "TOTAL_COBRO_CALCULADO": "Total cobrado",
                "ALQUILER_VAR_PASAJEROS": "Cobro pasajeros",
                "ALQUILER_VAR_VENTAS": "Cobro ventas",
            }
            variation_tab1 = compute_variation_summary(
                compare_summary_tab1,
                list(compare_labels_tab1.keys()),
            )
            render_variation_cards(
                variation_tab1,
                compare_labels_tab1,
                "Variación automática frente al año anterior seleccionado",
            )

            compare_table_tab1 = compare_summary_tab1.rename(
                columns={
                    "ANIO_LABEL": "Año",
                    "CICLO_1_PASAJEROS": "Ciclo 2",
                    "CICLO_2_VENTAS": "Ciclo 3",
                    "TOTAL_COBRO_CALCULADO": "Total cobrado",
                    "ALQUILER_VAR_PASAJEROS": "Cobro pasajeros",
                    "ALQUILER_VAR_VENTAS": "Cobro ventas",
                }
            )
            st.dataframe(compare_table_tab1, use_container_width=True, hide_index=True)

            variation_display_tab1 = build_variation_display_table(variation_tab1, compare_labels_tab1)
            if isinstance(variation_display_tab1, pd.DataFrame) and not variation_display_tab1.empty:
                st.dataframe(variation_display_tab1, use_container_width=True, hide_index=True)

with tab2:
    st.markdown('<div class="section-label">Análisis mensual por cliente</div>', unsafe_allow_html=True)
    variation_display_cliente = pd.DataFrame()

    selected_cliente_tab = st.selectbox(
        "Filtrar por inquilino",
        options=cliente_options,
        index=0 if default_cliente else None,
        key="cliente_tab_filter",
    )

    cliente_df = filtered[filtered["INQUILINO"] == selected_cliente_tab].copy() if selected_cliente_tab else filtered.iloc[0:0].copy()
    cliente_df = render_month_filter(cliente_df, "Meses a visualizar para el cliente", "tab2_months")

    cliente_monthly = (
        cliente_df.groupby(["PERIODO_MES", "PERIODO_LABEL"], as_index=False)[
            [
                "ALQUILER_VAR_PASAJEROS",
                "ALQUILER_VAR_VENTAS",
                "CICLO_1_PASAJEROS",
                "CICLO_2_VENTAS",
                "TOTAL_COBRO_CALCULADO",
                "VENTA_REPORTADA",
                "PASAJEROS",
            ]
        ]
        .sum()
        .sort_values("PERIODO_MES")
    )

    cliente_profile = {}
    if not cliente_df.empty:
        acuerdo_ventas_vals = sorted(cliente_df["ACUERDO_VENTAS"].dropna().astype(int).astype(str).unique().tolist())
        acuerdo_immg_vals = sorted(cliente_df["ACUERDO_IMMG"].dropna().astype(int).astype(str).unique().tolist())
        contratos_vals = sorted(cliente_df["CONTRATO"].dropna().astype(str).unique().tolist())
        locales_vals = sorted(cliente_df["LOCAL"].dropna().astype(str).unique().tolist())
        nom_vals = sorted(cliente_df["NOMENCLATURA"].dropna().astype(str).unique().tolist())

        cliente_profile = {
            "acuerdo_ventas": ", ".join(acuerdo_ventas_vals) if acuerdo_ventas_vals else "Sin dato",
            "acuerdo_immg": ", ".join(acuerdo_immg_vals) if acuerdo_immg_vals else "Sin dato",
            "contratos": ", ".join(contratos_vals[:4]) + (" ..." if len(contratos_vals) > 4 else ""),
            "locales": ", ".join(locales_vals[:5]) + (" ..." if len(locales_vals) > 5 else ""),
            "nomenclaturas": ", ".join(nom_vals[:3]) + (" ..." if len(nom_vals) > 3 else ""),
            "meses": cliente_df["PERIODO_LABEL"].nunique(),
            "total_cobrado": cliente_df["TOTAL_COBRO_CALCULADO"].sum(),
            "total_pasajeros": cliente_df["ALQUILER_VAR_PASAJEROS"].sum(),
            "total_ventas": cliente_df["ALQUILER_VAR_VENTAS"].sum(),
            "meses_con_ciclo_3": int(cliente_df["VENTAS_SUPERA_PASAJEROS"].sum()),
        }

    if cliente_df.empty:
        st.warning("No hay información disponible para el cliente seleccionado con los filtros actuales.")
    else:
        info_cols = st.columns(4)
        with info_cols[0]:
            render_info_card("Cliente", selected_cliente_tab, f"Meses analizados: {cliente_profile['meses']}")
        with info_cols[1]:
            render_info_card("Acuerdo ventas", cliente_profile["acuerdo_ventas"], "Código(s) asociado(s) al cobro por ventas")
        with info_cols[2]:
            render_info_card("Acuerdo IMMG", cliente_profile["acuerdo_immg"], "Código(s) asociado(s) al cobro por pasajeros")
        with info_cols[3]:
            render_info_card("Locales", cliente_profile["locales"], cliente_profile["nomenclaturas"])

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Cobro total del cliente", format_currency(cliente_profile["total_cobrado"]))
        k2.metric("Cobro acumulado por pasajeros", format_currency(cliente_profile["total_pasajeros"]))
        k3.metric("Cobro acumulado por ventas", format_currency(cliente_profile["total_ventas"]))
        k4.metric("Meses con ciclo 3", format_number(cliente_profile["meses_con_ciclo_3"]))

        g1, g2 = st.columns([1.2, 1])
        with g1:
            cliente_melt = cliente_monthly.melt(
                id_vars="PERIODO_LABEL",
                value_vars=["ALQUILER_VAR_PASAJEROS", "ALQUILER_VAR_VENTAS"],
                var_name="TIPO_COBRO",
                value_name="VALOR",
            )
            cliente_melt["TIPO_COBRO"] = cliente_melt["TIPO_COBRO"].replace(
                {
                    "ALQUILER_VAR_PASAJEROS": "Cobro por pasajeros",
                    "ALQUILER_VAR_VENTAS": "Cobro por ventas",
                }
            )
            fig_cliente = px.bar(
                cliente_melt,
                x="PERIODO_LABEL",
                y="VALOR",
                color="TIPO_COBRO",
                barmode="group",
                title=f"Cobros mes a mes de {selected_cliente_tab}",
                labels={"PERIODO_LABEL": "Periodo", "VALOR": "Valor", "TIPO_COBRO": "Tipo de cobro"},
                color_discrete_map={
                    "Cobro por pasajeros": COLORS["neon_cyan"],
                    "Cobro por ventas": COLORS["neon_magenta"],
                },
            )
            st.plotly_chart(style_plot(fig_cliente), use_container_width=True)

        with g2:
            fig_total_cliente = px.line(
                cliente_monthly,
                x="PERIODO_LABEL",
                y=["CICLO_1_PASAJEROS", "CICLO_2_VENTAS", "TOTAL_COBRO_CALCULADO"],
                markers=True,
                title="Ciclo 2, ciclo 3 y total cobrado",
                labels={"PERIODO_LABEL": "Periodo", "value": "Valor", "variable": "Componente"},
                color_discrete_map={
                    "CICLO_1_PASAJEROS": COLORS["neon_cyan"],
                    "CICLO_2_VENTAS": COLORS["neon_magenta"],
                    "TOTAL_COBRO_CALCULADO": COLORS["neon_green"],
                },
            )
            st.plotly_chart(style_plot(fig_total_cliente), use_container_width=True)

        g3, g4 = st.columns([1, 1])
        with g3:
            fig_pasajeros = px.bar(
                cliente_monthly,
                x="PERIODO_LABEL",
                y="PASAJEROS",
                title="Número de pasajeros por mes",
                labels={"PERIODO_LABEL": "Periodo", "PASAJEROS": "Pasajeros"},
                color_discrete_sequence=[COLORS["neon_cyan"]],
            )
            st.plotly_chart(style_plot(fig_pasajeros), use_container_width=True)

        with g4:
            cliente_monthly["DIFERENCIA_VENTAS_MENOS_PASAJEROS"] = (
                cliente_monthly["ALQUILER_VAR_VENTAS"] - cliente_monthly["ALQUILER_VAR_PASAJEROS"]
            )
            fig_dif = px.bar(
                cliente_monthly,
                x="PERIODO_LABEL",
                y="DIFERENCIA_VENTAS_MENOS_PASAJEROS",
                title="Diferencia mensual: ventas - pasajeros",
                labels={"PERIODO_LABEL": "Periodo", "DIFERENCIA_VENTAS_MENOS_PASAJEROS": "Diferencia ventas - pasajeros"},
                color_discrete_sequence=[COLORS["neon_magenta"]],
            )
            st.plotly_chart(style_plot(fig_dif), use_container_width=True)

        st.markdown('<div class="section-label">Detalle mensual del cliente</div>', unsafe_allow_html=True)
        cliente_table = cliente_monthly.copy()
        cliente_table.insert(1, "INQUILINO", selected_cliente_tab)
        cliente_table["ACUERDO_VENTAS"] = cliente_profile["acuerdo_ventas"]
        cliente_table["ACUERDO_IMMG"] = cliente_profile["acuerdo_immg"]
        cliente_table = cliente_table.rename(
            columns={
                "PERIODO_LABEL": "Periodo",
                "ALQUILER_VAR_PASAJEROS": "Cobro pasajeros",
                "ALQUILER_VAR_VENTAS": "Cobro ventas",
                "CICLO_1_PASAJEROS": "Ciclo 2",
                "CICLO_2_VENTAS": "Ciclo 3",
                "TOTAL_COBRO_CALCULADO": "Total cobrado",
                "VENTA_REPORTADA": "Venta reportada",
                "PASAJEROS": "Pasajeros",
                "ACUERDO_VENTAS": "Acuerdo ventas",
                "ACUERDO_IMMG": "Acuerdo IMMG",
            }
        )
        st.dataframe(cliente_table, use_container_width=True, hide_index=True)
        compare_cliente = render_same_month_comparison(
            cliente_df,
            "tab2_cliente",
            "Comparativa del mismo mes entre años para este cliente"
        )

        if not compare_cliente.empty:
            compare_cliente_summary = (
                compare_cliente.groupby(["PERIODO_ANIO", "ANIO_LABEL"], as_index=False)[
                    ["CICLO_1_PASAJEROS", "CICLO_2_VENTAS", "TOTAL_COBRO_CALCULADO", "PASAJEROS", "VENTA_REPORTADA"]
                ]
                .sum()
                .sort_values("PERIODO_ANIO")
            )

            h1, h2 = st.columns([1.1, 1])
            with h1:
                cliente_compare_melt = compare_cliente_summary.melt(
                    id_vars="ANIO_LABEL",
                    value_vars=["CICLO_1_PASAJEROS", "CICLO_2_VENTAS", "TOTAL_COBRO_CALCULADO"],
                    var_name="COMPONENTE",
                    value_name="VALOR",
                )
                cliente_compare_melt["COMPONENTE"] = cliente_compare_melt["COMPONENTE"].replace(
                    {
                        "CICLO_1_PASAJEROS": "Ciclo 2",
                        "CICLO_2_VENTAS": "Ciclo 3",
                        "TOTAL_COBRO_CALCULADO": "Total cobrado",
                    }
                )
                fig_compare_cliente_1 = px.bar(
                    cliente_compare_melt,
                    x="ANIO_LABEL",
                    y="VALOR",
                    color="COMPONENTE",
                    barmode="group",
                    title=f"Comparativo anual del mismo mes para {selected_cliente_tab}",
                    labels={"ANIO_LABEL": "Año", "VALOR": "Valor", "COMPONENTE": "Componente"},
                    color_discrete_map={
                        "Ciclo 2": COLORS["neon_cyan"],
                        "Ciclo 3": COLORS["neon_magenta"],
                        "Total cobrado": COLORS["neon_green"],
                    },
                )
                st.plotly_chart(style_plot(fig_compare_cliente_1), use_container_width=True)

            with h2:
                fig_compare_cliente_2 = make_subplots(specs=[[{"secondary_y": True}]])
                fig_compare_cliente_2.add_trace(
                    go.Bar(
                        x=compare_cliente_summary["ANIO_LABEL"],
                        y=compare_cliente_summary["PASAJEROS"],
                        name="Pasajeros",
                        marker_color=COLORS["neon_cyan"],
                        text=compare_cliente_summary["PASAJEROS"].map(format_number),
                        textposition="outside",
                        opacity=0.85,
                    ),
                    secondary_y=False,
                )
                fig_compare_cliente_2.add_trace(
                    go.Scatter(
                        x=compare_cliente_summary["ANIO_LABEL"],
                        y=compare_cliente_summary["VENTA_REPORTADA"],
                        name="Venta reportada",
                        mode="lines+markers+text",
                        line=dict(color=COLORS["neon_magenta"], width=3),
                        marker=dict(color=COLORS["neon_magenta"], size=9),
                        text=compare_cliente_summary["VENTA_REPORTADA"].map(format_currency),
                        textposition="top center",
                    ),
                    secondary_y=True,
                )
                fig_compare_cliente_2.update_layout(
                    title="Pasajeros vs venta reportada por año",
                    bargap=0.35,
                )
                fig_compare_cliente_2.update_xaxes(title_text="Año")
                fig_compare_cliente_2.update_yaxes(title_text="Pasajeros", secondary_y=False)
                fig_compare_cliente_2.update_yaxes(title_text="Venta reportada", secondary_y=True)
                st.plotly_chart(style_plot(fig_compare_cliente_2), use_container_width=True)

                if len(compare_cliente_summary) >= 2:
                    base_row = compare_cliente_summary.sort_values("PERIODO_ANIO").iloc[-2]
                    current_row = compare_cliente_summary.sort_values("PERIODO_ANIO").iloc[-1]
                    delta_pas = current_row["PASAJEROS"] - base_row["PASAJEROS"]
                    delta_venta = current_row["VENTA_REPORTADA"] - base_row["VENTA_REPORTADA"]
                    pct_pas = (delta_pas / base_row["PASAJEROS"] * 100) if base_row["PASAJEROS"] else np.nan
                    pct_venta = (delta_venta / base_row["VENTA_REPORTADA"] * 100) if base_row["VENTA_REPORTADA"] else np.nan

                    resumen_pas = (
                        f"Pasajeros {'subió' if delta_pas >= 0 else 'bajó'} {format_number(abs(delta_pas))}"
                        + (f" ({pct_pas:+.1f}%)." if not pd.isna(pct_pas) else ".")
                    )
                    resumen_venta = (
                        f" Venta reportada {'subió' if delta_venta >= 0 else 'bajó'} {format_currency(abs(delta_venta))}"
                        + (f" ({pct_venta:+.1f}%)." if not pd.isna(pct_venta) else ".")
                    )
                    st.markdown(
                        f"<div class='note'><b>Lectura ejecutiva:</b> {resumen_pas}{resumen_venta}</div>",
                        unsafe_allow_html=True,
                    )

            compare_labels_cliente = {
                "CICLO_1_PASAJEROS": "Ciclo 2",
                "CICLO_2_VENTAS": "Ciclo 3",
                "TOTAL_COBRO_CALCULADO": "Total cobrado",
                "PASAJEROS": "Pasajeros",
                "VENTA_REPORTADA": "Venta reportada",
            }
            variation_cliente = compute_variation_summary(
                compare_cliente_summary,
                list(compare_labels_cliente.keys()),
            )
            render_variation_cards(
                variation_cliente,
                compare_labels_cliente,
                f"Variación automática para {selected_cliente_tab} frente al año anterior seleccionado",
            )

            compare_cliente_table = compare_cliente_summary.rename(
                columns={
                    "ANIO_LABEL": "Año",
                    "CICLO_1_PASAJEROS": "Ciclo 2",
                    "CICLO_2_VENTAS": "Ciclo 3",
                    "TOTAL_COBRO_CALCULADO": "Total cobrado",
                    "PASAJEROS": "Pasajeros",
                    "VENTA_REPORTADA": "Venta reportada",
                }
            )
            st.dataframe(compare_cliente_table, use_container_width=True, hide_index=True)

            variation_display_cliente = build_variation_display_table(variation_cliente, compare_labels_cliente)
            if isinstance(variation_display_cliente, pd.DataFrame) and not variation_display_cliente.empty:
                st.dataframe(variation_display_cliente, use_container_width=True, hide_index=True)

with tab3:
    st.markdown('<div class="section-label">Consolidado y ranking por inquilino</div>', unsafe_allow_html=True)
    tab3_filtered = render_month_filter(filtered, "Meses a visualizar en consolidado", "tab3_months")

    if tab3_filtered.empty:
        st.warning("No hay datos para los meses seleccionados en esta sección.")
    else:
        top_inquilinos_tab3 = (
            tab3_filtered.groupby(["INQUILINO", "ACUERDO_VENTAS", "ACUERDO_IMMG"], dropna=False, as_index=False)[
                ["CICLO_1_PASAJEROS", "CICLO_2_VENTAS", "TOTAL_COBRO_CALCULADO", "ALQUILER_VAR_VENTAS", "ALQUILER_VAR_PASAJEROS"]
            ]
            .sum()
            .sort_values("TOTAL_COBRO_CALCULADO", ascending=False)
        )

        slider_max = max(5, min(30, len(top_inquilinos_tab3)))
        slider_default = min(10, slider_max)

        top_n = st.slider(
            "Cantidad de inquilinos a visualizar",
            min_value=5,
            max_value=slider_max,
            value=slider_default,
            key="ranking_inquilinos",
        )
        top_view = top_inquilinos_tab3.head(top_n).copy()

        fig6 = px.bar(
            top_view,
            x="TOTAL_COBRO_CALCULADO",
            y="INQUILINO",
            color="INQUILINO",
            orientation="h",
            title="Ranking de inquilinos por cobro total",
            labels={"TOTAL_COBRO_CALCULADO": "Total cobrado", "INQUILINO": "Inquilino"},
        )
        fig6.update_layout(showlegend=False)
        st.plotly_chart(style_plot(fig6), use_container_width=True)

        fig7_df = top_view.melt(
            id_vars=["INQUILINO"],
            value_vars=["ALQUILER_VAR_PASAJEROS", "ALQUILER_VAR_VENTAS"],
            var_name="COMPONENTE",
            value_name="VALOR",
        )
        fig7_df["COMPONENTE"] = fig7_df["COMPONENTE"].replace(
            {
                "ALQUILER_VAR_PASAJEROS": "Base pasajeros",
                "ALQUILER_VAR_VENTAS": "Valor ventas",
            }
        )
        fig7 = px.bar(
            fig7_df,
            x="INQUILINO",
            y="VALOR",
            color="COMPONENTE",
            barmode="group",
            title="Comparativo base por pasajeros vs componente por ventas",
            labels={"INQUILINO": "Inquilino", "VALOR": "Valor", "COMPONENTE": "Componente"},
            color_discrete_map={"Base pasajeros": COLORS["neon_cyan"], "Valor ventas": COLORS["neon_magenta"]},
        )
        st.plotly_chart(style_plot(fig7), use_container_width=True)

        display_inquilinos = top_inquilinos_tab3.copy()
        display_inquilinos["ACUERDO_VENTAS"] = display_inquilinos["ACUERDO_VENTAS"].fillna(0).astype(int).astype(str)
        display_inquilinos["ACUERDO_IMMG"] = display_inquilinos["ACUERDO_IMMG"].fillna(0).astype(int).astype(str)
        display_inquilinos = display_inquilinos.rename(
            columns={
                "INQUILINO": "Inquilino",
                "ACUERDO_VENTAS": "Acuerdo ventas",
                "ACUERDO_IMMG": "Acuerdo IMMG",
                "CICLO_1_PASAJEROS": "Ciclo 2",
                "CICLO_2_VENTAS": "Ciclo 3",
                "TOTAL_COBRO_CALCULADO": "Total cobrado",
                "ALQUILER_VAR_PASAJEROS": "Base pasajeros",
                "ALQUILER_VAR_VENTAS": "Valor ventas",
            }
        )
        st.dataframe(display_inquilinos, use_container_width=True, hide_index=True)

with tab4:
    tab4_filtered = render_month_filter(filtered, "Meses a validar", "tab4_months")

    if tab4_filtered.empty:
        st.warning("No hay datos para los meses seleccionados en esta sección.")
    else:
        total_rows = len(tab4_filtered)
        ok_ventas = int(tab4_filtered["VALIDA_ALQ_VENTAS"].sum())
        ok_pas = int(tab4_filtered["VALIDA_ALQ_PASAJEROS"].sum())
        ok_fact = int(tab4_filtered["VALIDA_FACTURADO_VARIABLE"].sum())
        ok_total = int(tab4_filtered["VALIDA_TOTAL_COBRO"].sum())

        st.markdown('<div class="section-label">Estado de consistencia de cálculos</div>', unsafe_allow_html=True)

        badge_html = f"""
        <div class="card">
            <span class="{'ok-badge' if ok_ventas == total_rows else 'warn-badge'}">Alquiler ventas: {ok_ventas}/{total_rows}</span>
            <span class="{'ok-badge' if ok_pas == total_rows else 'warn-badge'}">Alquiler pasajeros: {ok_pas}/{total_rows}</span>
            <span class="{'ok-badge' if ok_fact == total_rows else 'warn-badge'}">Facturado variable: {ok_fact}/{total_rows}</span>
            <span class="{'ok-badge' if ok_total == total_rows else 'warn-badge'}">Total cobro: {ok_total}/{total_rows}</span>
            <div class="small" style="margin-top:0.6rem;">
                Estas validaciones comparan los valores reportados del archivo contra los cálculos esperados según la lógica del negocio.
            </div>
        </div>
        """
        st.markdown(badge_html, unsafe_allow_html=True)

        inconsistencias = tab4_filtered[
            ~(
                tab4_filtered["VALIDA_ALQ_VENTAS"]
                & tab4_filtered["VALIDA_ALQ_PASAJEROS"]
                & tab4_filtered["VALIDA_FACTURADO_VARIABLE"]
                & tab4_filtered["VALIDA_TOTAL_COBRO"]
            )
        ].copy()

        if inconsistencias.empty:
            st.success("No se encontraron inconsistencias con los filtros actuales.")
        else:
            cols_show = [
                "PERIODO_LABEL", "CONTRATO", "INQUILINO", "LOCAL", "ACUERDO_VENTAS", "ACUERDO_IMMG",
                "TASA_VENTAS", "VENTA_REPORTADA", "ALQUILER_VAR_VENTAS",
                "TASA_PASAJEROS", "PASAJEROS", "ALQUILER_VAR_PASAJEROS",
                "FACTURADO_VARIABLE", "CICLO_1_PASAJEROS", "CICLO_2_VENTAS", "TOTAL_COBRO_CALCULADO",
                "VALIDA_ALQ_VENTAS", "VALIDA_ALQ_PASAJEROS", "VALIDA_FACTURADO_VARIABLE", "VALIDA_TOTAL_COBRO"
            ]
            st.warning("Se encontraron registros con diferencias frente a los cálculos esperados.")
            st.dataframe(inconsistencias[cols_show], use_container_width=True, hide_index=True)

with tab5:
    st.markdown('<div class="section-label">Detalle operativo filtrado</div>', unsafe_allow_html=True)
    detail = render_month_filter(filtered, "Meses a visualizar en el detalle", "tab5_months")

    if detail.empty:
        st.warning("No hay datos para los meses seleccionados en esta sección.")
    else:
        detail["ACUERDO_VENTAS"] = detail["ACUERDO_VENTAS"].fillna(0).astype(int).astype(str)
        detail["ACUERDO_IMMG"] = detail["ACUERDO_IMMG"].fillna(0).astype(int).astype(str)

        final_cols = [
            "PERIODO_LABEL",
            "CONTRATO",
            "INQUILINO",
            "NOMENCLATURA",
            "LOCAL",
            "ACUERDO_VENTAS",
            "ACUERDO_IMMG",
            "TASA_VENTAS",
            "VENTA_REPORTADA",
            "ALQUILER_VAR_VENTAS",
            "TASA_PASAJEROS",
            "PASAJEROS",
            "ALQUILER_VAR_PASAJEROS",
            "FACTURADO_VARIABLE",
            "CICLO_1_PASAJEROS",
            "CICLO_2_VENTAS",
            "TOTAL_COBRO_CALCULADO",
        ]
        st.dataframe(detail[final_cols], use_container_width=True, hide_index=True)

        st.download_button(
            label="Descargar detalle procesado",
            data=build_download(detail),
            file_name="detalle_cobro_variable_procesado.csv",
            mime="text/csv",
        )
