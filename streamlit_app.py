from pathlib import Path
import sys

import streamlit as st


RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from automates.ui import (  # noqa: E402
    render_automates,
    render_controles,
    render_dashboard,
    render_indicadores,
    render_inicio,
    render_vencimientos,
)


st.set_page_config(page_title="Portafolio | Datos y Tesorería", page_icon="📊", layout="wide")
st.sidebar.title("Flujo de trabajo")
sección = st.sidebar.radio(
    "Módulo",
    [
        "Inicio",
        "Centro de reportes",
        "Posición bancaria",
        "Indicadores económicos",
        "Vencimientos y fondeo",
        "Control y trazabilidad",
    ],
)
st.sidebar.caption("Datos y entidades 100% sintéticos")

if sección == "Centro de reportes":
    render_automates()
elif sección == "Posición bancaria":
    render_dashboard()
elif sección == "Indicadores económicos":
    render_indicadores()
elif sección == "Vencimientos y fondeo":
    render_vencimientos()
elif sección == "Control y trazabilidad":
    render_controles()
else:
    render_inicio()
