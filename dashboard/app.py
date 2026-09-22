from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from automates.core import calcular_brecha_liquidez, construir_maestro_pasivos, construir_reporte_cartera  # noqa: E402


DATOS = RAIZ / "data" / "synthetic"
st.set_page_config(page_title="Tesorería y Fondeo | Demo", layout="wide")
st.title("Dashboard de Tesorería y Fondeo")
st.caption("Reconstrucción pública con datos 100% sintéticos")

requeridos = ["posicion_flujo.csv", "estados_financieros.csv", "pasivos.csv", "cartera.csv"]
if any(not (DATOS / nombre).exists() for nombre in requeridos):
    st.error("Primero ejecuta: python scripts/generar_datos_sinteticos.py")
    st.stop()

posiciones = pd.read_csv(DATOS / "posicion_flujo.csv", parse_dates=["fecha"])
estados = pd.read_csv(DATOS / "estados_financieros.csv")
pasivos = construir_maestro_pasivos(pd.read_csv(DATOS / "pasivos.csv"))
cartera = construir_reporte_cartera(pd.read_csv(DATOS / "cartera.csv"))
brecha = calcular_brecha_liquidez(estados, pasivos)

tab1, tab2, tab3, tab4 = st.tabs(["Posición bancaria", "Brecha de liquidez", "Pasivos", "Cartera"])
with tab1:
    bancos = st.multiselect("Bancos", sorted(posiciones["banco"].unique()), default=sorted(posiciones["banco"].unique()))
    filtrados = posiciones[posiciones["banco"].isin(bancos)]
    entradas = filtrados["entradas"].sum()
    salidas = filtrados["salidas"].sum()
    saldo = filtrados.groupby("banco")["saldo_final"].last().sum()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Entradas", f"${entradas:,.0f}")
    c2.metric("Salidas", f"${salidas:,.0f}")
    c3.metric("Flujo neto", f"${entradas - salidas:,.0f}")
    c4.metric("Posición final", f"${saldo:,.0f}")
    diario = filtrados.groupby("fecha", as_index=False)[["entradas", "salidas"]].sum()
    diario["flujo_neto"] = diario["entradas"] - diario["salidas"]
    st.plotly_chart(px.line(diario, x="fecha", y="flujo_neto", title="Flujo neto diario"), use_container_width=True)
with tab2:
    st.plotly_chart(px.bar(brecha, x="horizonte", y=["activos", "pasivos", "brecha"], barmode="group", title="Brecha por horizonte"), use_container_width=True)
    st.dataframe(brecha, use_container_width=True, hide_index=True)
with tab3:
    st.plotly_chart(px.bar(pasivos, x="fondeador", y="total", title="Pasivos por fondeador"), use_container_width=True)
    st.dataframe(pasivos, use_container_width=True, hide_index=True)
with tab4:
    resumen = cartera.groupby(["producto", "estatus"], as_index=False)["saldo_total"].sum()
    st.plotly_chart(px.bar(resumen, x="producto", y="saldo_total", color="estatus", barmode="group"), use_container_width=True)
    st.dataframe(cartera.head(30), use_container_width=True, hide_index=True)

