from pathlib import Path
import sys

import streamlit as st


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from automates.ui import render_dashboard  # noqa: E402


st.set_page_config(page_title="Tesorería y Fondeo | Demo", page_icon="📈", layout="wide")
render_dashboard()
