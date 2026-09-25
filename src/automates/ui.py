from __future__ import annotations

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
import plotly.express as px
import streamlit as st

from .core import calcular_brecha_liquidez, construir_maestro_pasivos, construir_reporte_cartera
from .demo_data import generar_datasets, guardar_datasets
from .pipeline import ejecutar_pipeline


MORADO = "#4B286D"


@st.cache_data(show_spinner=False)
def cargar_demo(seed: int = 2027) -> dict[str, pd.DataFrame]:
    return generar_datasets(seed)


@st.cache_data(show_spinner="Generando 39 reportes financieros ficticios...")
def preparar_automates(seed: int = 2027) -> dict[str, object]:
    with TemporaryDirectory(prefix="automates_demo_") as temporal:
        raiz = Path(temporal)
        datos = raiz / "data"
        salida = raiz / "output"
        guardar_datasets(datos, seed)
        resultado = ejecutar_pipeline(datos, salida)

        paquete = BytesIO()
        with ZipFile(paquete, "w", ZIP_DEFLATED) as archivo_zip:
            for archivo in sorted(salida.rglob("*")):
                if archivo.is_file():
                    archivo_zip.write(archivo, archivo.relative_to(salida))

        return {
            "tablas": resultado["tablas"],
            "bitacora": resultado["bitacora"],
            "cantidad_reportes": resultado["cantidad_reportes"],
            "zip": paquete.getvalue(),
            "archivos_zip": len(ZipFile(BytesIO(paquete.getvalue())).namelist()),
        }


def _formato_moneda(valor: float) -> str:
    return f"${valor:,.0f}"


def render_inicio() -> None:
    st.title("Portafolio de Datos, BI y Tesorería")
    st.subheader("Abraham Ramsés Gutiérrez Valdés")
    st.write(
        "Demostración pública de automatización financiera y visualización de tesorería. "
        "Todo el contenido se genera con datos sintéticos y reglas representativas."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reportes", "39")
    c2.metric("Fondeadores demo", "13")
    c3.metric("Reducción relacionada", "75%")
    c4.metric("Pruebas", "8")
    st.markdown(
        """
        ### Qué puede revisar un reclutador

        - **AutomaTES:** proceso ETL, cinco entregables principales, bitácora y 39 reportes descargables.
        - **Dashboard:** posición bancaria, flujo neto, brecha de liquidez, pasivos y cartera.
        - **Código:** validaciones, transformaciones con pandas, exportación a Excel y pruebas automáticas.
        - **Privacidad:** instituciones, clientes, montos y fechas completamente ficticios.
        """
    )
    st.info("Selecciona una aplicación en el menú lateral.")


def render_automates() -> None:
    st.title("AutomaTES | Automatización de reportes")
    st.caption("Reconstrucción pública con datos 100% sintéticos")
    st.warning(
        "Esta demostración no acepta archivos externos y no contiene plantillas, reglas ni datos de ningún empleador."
    )

    resultado = preparar_automates()
    tablas: dict[str, pd.DataFrame] = resultado["tablas"]  # type: ignore[assignment]
    bitacora: pd.DataFrame = resultado["bitacora"]  # type: ignore[assignment]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Entregables principales", len(tablas))
    c2.metric("Reportes por fondeador", int(resultado["cantidad_reportes"]))
    c3.metric("Fondeadores ficticios", "13")
    c4.metric("Archivos descargables", int(resultado["archivos_zip"]))
    c5.metric("Validaciones", "Correctas")

    st.success("Pipeline ejecutado: limpieza, homologación, validación, transformación y exportación completadas.")
    st.download_button(
        "Descargar resultados sintéticos (.zip)",
        data=resultado["zip"],
        file_name="automates_resultados_sinteticos.zip",
        mime="application/zip",
        width="stretch",
    )

    nombres = {
        "estados_financieros_base.xlsx": "Estados Financieros Base",
        "maestro_pasivos_base.xlsx": "Maestro de Pasivos Base",
        "reporte_cartera.xlsx": "Reporte de Cartera",
        "brecha_liquidez.xlsx": "Brecha de Liquidez",
        "comparativo_trazabilidad.xlsx": "Trazabilidad",
    }
    pestañas = st.tabs([*nombres.values(), "Bitácora"])
    for pestaña, (archivo, etiqueta) in zip(pestañas[:-1], nombres.items()):
        with pestaña:
            st.subheader(etiqueta)
            st.dataframe(tablas[archivo], width="stretch", hide_index=True)
    with pestañas[-1]:
        st.subheader("Bitácora de ejecución")
        st.dataframe(bitacora, width="stretch", hide_index=True)


def render_dashboard() -> None:
    st.title("Dashboard de Tesorería y Fondeo")
    st.caption("Posición, flujo, liquidez, pasivos y cartera con datos 100% sintéticos")
    datos = cargar_demo()
    posiciones = datos["posicion_flujo.csv"].copy()
    posiciones["fecha"] = pd.to_datetime(posiciones["fecha"])
    estados = datos["estados_financieros.csv"]
    pasivos = construir_maestro_pasivos(datos["pasivos.csv"])
    cartera = construir_reporte_cartera(datos["cartera.csv"])
    brecha = calcular_brecha_liquidez(estados, pasivos)

    tab1, tab2, tab3, tab4 = st.tabs(["Posición bancaria", "Brecha de liquidez", "Pasivos", "Cartera"])
    with tab1:
        bancos_disponibles = sorted(posiciones["banco"].unique())
        bancos = st.multiselect("Bancos", bancos_disponibles, default=bancos_disponibles)
        filtrados = posiciones[posiciones["banco"].isin(bancos)]
        entradas = float(filtrados["entradas"].sum())
        salidas = float(filtrados["salidas"].sum())
        saldo = float(filtrados.groupby("banco")["saldo_final"].last().sum()) if not filtrados.empty else 0.0
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Entradas", _formato_moneda(entradas))
        c2.metric("Salidas", _formato_moneda(salidas))
        c3.metric("Flujo neto", _formato_moneda(entradas - salidas))
        c4.metric("Posición final", _formato_moneda(saldo))
        diario = filtrados.groupby("fecha", as_index=False)[["entradas", "salidas"]].sum()
        diario["flujo_neto"] = diario["entradas"] - diario["salidas"]
        figura = px.line(diario, x="fecha", y="flujo_neto", title="Flujo neto diario", color_discrete_sequence=[MORADO])
        st.plotly_chart(figura, width="stretch")
    with tab2:
        figura = px.bar(
            brecha,
            x="horizonte",
            y=["activos", "pasivos", "brecha"],
            barmode="group",
            title="Brecha por horizonte",
            color_discrete_sequence=["#4B286D", "#8C68A8", "#2F8F9D"],
        )
        st.plotly_chart(figura, width="stretch")
        st.dataframe(brecha, width="stretch", hide_index=True)
    with tab3:
        figura = px.bar(
            pasivos,
            x="fondeador",
            y="total",
            title="Pasivos por fondeador",
            color_discrete_sequence=[MORADO],
        )
        st.plotly_chart(figura, width="stretch")
        st.dataframe(pasivos, width="stretch", hide_index=True)
    with tab4:
        resumen = cartera.groupby(["producto", "estatus"], as_index=False)["saldo_total"].sum()
        figura = px.bar(
            resumen,
            x="producto",
            y="saldo_total",
            color="estatus",
            barmode="group",
            title="Cartera por producto y estatus",
            color_discrete_sequence=[MORADO, "#D98C5F"],
        )
        st.plotly_chart(figura, width="stretch")
        st.dataframe(cartera.head(30), width="stretch", hide_index=True)
