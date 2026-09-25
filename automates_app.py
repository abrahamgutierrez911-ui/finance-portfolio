from pathlib import Path
import sys

import streamlit as st


RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from automates.ui import render_automates  # noqa: E402


st.set_page_config(page_title="AutomaTES | Demo", page_icon="⚙️", layout="wide")
render_automates()
