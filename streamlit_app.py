from pathlib import Path
import sys

import streamlit as st


RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from automates.ui import render_automates, render_dashboard, render_inicio  # noqa: E402


st.set_page_config(page_title="Portafolio | Datos y Tesorería", page_icon="📊", layout="wide")
st.sidebar.title("Portafolio")
sección = st.sidebar.radio("Aplicación", ["Inicio", "AutomaTES", "Dashboard"])
st.sidebar.caption("Datos y entidades 100% sintéticos")

if sección == "AutomaTES":
    render_automates()
elif sección == "Dashboard":
    render_dashboard()
else:
    render_inicio()
