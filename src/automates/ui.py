from __future__ import annotations

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
import plotly.express as px
import streamlit as st

from .controls import calendario_vencimientos, conciliacion_reportada, matriz_controles, uso_lineas
from .core import calcular_brecha_liquidez, construir_maestro_pasivos, construir_reporte_cartera
from .demo_data import generar_datasets, guardar_datasets
from .pipeline import ejecutar_pipeline


MORADO = "#4B286D"
AZUL = "#075985"
VERDE = "#0F9D76"


@st.cache_data(show_spinner=False)
def cargar_demo(seed: int = 2027) -> dict[str, pd.DataFrame]:
    return generar_datasets(seed)


@st.cache_data(show_spinner="Ejecutando controles y generando el paquete demostrativo...")
def preparar_automates(seed: int = 2027) -> dict[str, object]:
    with TemporaryDirectory(prefix="automates_demo_") as temporal:
        raiz = Path(temporal)
        datos = raiz / "data"
        salida = raiz / "output"
        conteos = guardar_datasets(datos, seed)
        resultado = ejecutar_pipeline(datos, salida)

        paquete = BytesIO()
        with ZipFile(paquete, "w", ZIP_DEFLATED) as archivo_zip:
            for archivo in sorted(salida.rglob("*")):
                if archivo.is_file():
                    archivo_zip.write(archivo, archivo.relative_to(salida))
        archivos_zip = len(ZipFile(BytesIO(paquete.getvalue())).namelist())
        return {
            "tablas": resultado["tablas"],
            "bitacora": resultado["bitacora"],
            "cantidad_reportes": resultado["cantidad_reportes"],
            "zip": paquete.getvalue(),
            "archivos_zip": archivos_zip,
            "conteos_insumos": conteos,
        }


def _formato_moneda(valor: float) -> str:
    if abs(valor) >= 1_000_000:
        return f"${valor / 1_000_000:,.1f} M"
    return f"${valor:,.0f}"


def _inventario_insumos(conteos: dict[str, int]) -> pd.DataFrame:
    nombres = {
        "posicion_flujo.csv": "Posición y flujo bancario",
        "estados_financieros.csv": "Estados financieros",
        "pasivos.csv": "Pasivos y vencimientos",
        "cartera.csv": "Base de cartera",
        "indicadores_economicos.csv": "Indicadores económicos",
        "covenants.csv": "Covenants",
        "cifras_reportadas.csv": "Cifras reportadas",
    }
    return pd.DataFrame(
        [
            {
                "insumo": nombres[archivo],
                "archivo_demo": archivo,
                "filas": filas,
                "esquema": "Validado",
                "origen": "Generador sintético",
            }
            for archivo, filas in conteos.items()
        ]
    )


def render_inicio() -> None:
    st.title("Portafolio de Datos, BI y Tesorería")
    st.subheader("Abraham Ramsés Gutiérrez Valdés")
    st.write(
        "Reconstrucción pública de una solución modular para reportería financiera, posición bancaria, "
        "vencimientos, fondeo y control. La lógica y la información son exclusivamente demostrativas."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reportes especializados", "39")
    c2.metric("Fondeadores demo", "13")
    c3.metric("Archivos generados", "52")
    c4.metric("Reducción relacionada", "75%")
    st.markdown(
        """
        ### Recorrido recomendado

        1. **Centro de reportes:** revisa insumos, ejecución, controles, conciliación y exportaciones.
        2. **Posición bancaria:** explora movimientos por empresa, banco, moneda y categoría.
        3. **Indicadores:** consulta históricos simulados de tipo de cambio y tasas.
        4. **Vencimientos y fondeo:** analiza compromisos, líneas autorizadas y covenants.
        5. **Control y trazabilidad:** identifica excepciones y revisa la bitácora de punta a punta.
        """
    )
    st.info("La demo no acepta documentos laborales y se reconstruyó sin código, formatos ni reglas de terceros.")


def render_automates() -> None:
    st.title("Centro de reportes | AutomaTES")
    st.caption("Orquestación ETL, control financiero y reportería con datos 100% sintéticos")
    resultado = preparar_automates()
    tablas: dict[str, pd.DataFrame] = resultado["tablas"]  # type: ignore[assignment]
    bitacora: pd.DataFrame = resultado["bitacora"]  # type: ignore[assignment]
    conteos: dict[str, int] = resultado["conteos_insumos"]  # type: ignore[assignment]

    periodo = st.selectbox("Periodo demostrativo", ["Septiembre 2026", "Agosto 2026", "Julio 2026"])
    pasos = st.columns(4)
    for columna, numero, nombre, estado in zip(
        pasos,
        ["01", "02", "03", "04"],
        ["Periodo", "Insumos", "Controles", "Ejecución"],
        [periodo, "7 fuentes listas", "8 reglas ejecutadas", "Completada"],
    ):
        columna.markdown(f"**{numero} · {nombre}**")
        columna.caption(estado)
    st.progress(100, text="Pipeline completado: extracción, homologación, validación, conciliación y exportación")

    st.subheader("Insumos del proceso")
    st.dataframe(_inventario_insumos(conteos), width="stretch", hide_index=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Entregables principales", len(tablas))
    c2.metric("Reportes por fondeador", int(resultado["cantidad_reportes"]))
    c3.metric("Archivos descargables", int(resultado["archivos_zip"]))
    c4.metric("Controles ejecutados", len(tablas["matriz_controles.xlsx"]))
    st.download_button(
        "Descargar paquete de resultados sintéticos (.zip)",
        data=resultado["zip"],
        file_name="automates_paquete_control_sintetico.zip",
        mime="application/zip",
        width="stretch",
    )

    tabs = st.tabs(["Resumen", "Entregables", "Controles", "Conciliación", "Bitácora"])
    with tabs[0]:
        st.dataframe(tablas["resumen_ejecutivo.xlsx"], width="stretch", hide_index=True)
    with tabs[1]:
        seleccion = st.selectbox("Vista previa", list(tablas), key="entregable_preview")
        st.dataframe(tablas[seleccion], width="stretch", hide_index=True)
    with tabs[2]:
        controles = tablas["matriz_controles.xlsx"]
        st.dataframe(controles, width="stretch", hide_index=True)
    with tabs[3]:
        conciliacion = tablas["conciliacion_reportada.xlsx"]
        st.dataframe(conciliacion, width="stretch", hide_index=True)
    with tabs[4]:
        st.dataframe(bitacora, width="stretch", hide_index=True)


def _filtros_posicion(posiciones: pd.DataFrame) -> pd.DataFrame:
    c1, c2, c3, c4 = st.columns(4)
    empresas = c1.multiselect("Empresa", sorted(posiciones["empresa"].unique()), default=sorted(posiciones["empresa"].unique()))
    bancos = c2.multiselect("Banco", sorted(posiciones["banco"].unique()), default=sorted(posiciones["banco"].unique()))
    monedas = c3.multiselect("Moneda", sorted(posiciones["moneda"].unique()), default=sorted(posiciones["moneda"].unique()))
    categorias = c4.multiselect("Categoría", sorted(posiciones["categoria"].unique()), default=sorted(posiciones["categoria"].unique()))
    return posiciones[
        posiciones["empresa"].isin(empresas)
        & posiciones["banco"].isin(bancos)
        & posiciones["moneda"].isin(monedas)
        & posiciones["categoria"].isin(categorias)
    ]


def render_dashboard() -> None:
    st.title("Dashboard de Posición Bancaria")
    st.caption("Movimientos, comparativos y validaciones con datos sintéticos")
    datos = cargar_demo()
    posiciones = datos["posicion_flujo.csv"].copy()
    posiciones["fecha"] = pd.to_datetime(posiciones["fecha"])
    filtrados = _filtros_posicion(posiciones)

    entradas = float(filtrados["entradas"].sum())
    salidas = float(filtrados["salidas"].sum())
    finales = filtrados.sort_values("fecha").groupby(["banco", "empresa", "moneda"])["saldo_final"].last()
    saldo_final = float(finales.sum()) if not finales.empty else 0.0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total ingresos", _formato_moneda(entradas))
    c2.metric("Total egresos", _formato_moneda(salidas))
    c3.metric("Flujo neto", _formato_moneda(entradas - salidas))
    c4.metric("Posición final", _formato_moneda(saldo_final))

    tabs = st.tabs(["Movimientos", "Gráficas", "Comparativo", "Validación"])
    diario = filtrados.groupby("fecha", as_index=False)[["entradas", "salidas"]].sum()
    diario["flujo_neto"] = diario["entradas"] - diario["salidas"]
    with tabs[0]:
        st.dataframe(filtrados.tail(50), width="stretch", hide_index=True)
    with tabs[1]:
        figura = px.line(diario, x="fecha", y=["entradas", "salidas", "flujo_neto"], title="Evolución diaria")
        st.plotly_chart(figura, width="stretch")
    with tabs[2]:
        comparativo = filtrados.groupby(["empresa", "banco"], as_index=False)[["entradas", "salidas"]].sum()
        figura = px.bar(comparativo, x="banco", y=["entradas", "salidas"], color="empresa", barmode="group")
        st.plotly_chart(figura, width="stretch")
    with tabs[3]:
        filtrados = filtrados.copy()
        filtrados["diferencia"] = filtrados["saldo_inicial"] + filtrados["entradas"] - filtrados["salidas"] - filtrados["saldo_final"]
        st.metric("Movimientos con diferencia", int(filtrados["diferencia"].abs().gt(0.01).sum()))
        st.dataframe(filtrados[["operacion_id", "fecha", "banco", "saldo_final", "diferencia"]].tail(30), width="stretch", hide_index=True)


def render_indicadores() -> None:
    st.title("Indicadores Económicos")
    st.caption("Series offline simuladas; no representan cotizaciones oficiales ni actuales")
    indicadores = cargar_demo()["indicadores_economicos.csv"].copy()
    indicadores["fecha"] = pd.to_datetime(indicadores["fecha"])
    actuales = indicadores.sort_values("fecha").groupby("serie", as_index=False).tail(1)
    columnas = st.columns(len(actuales))
    for columna, (_, fila) in zip(columnas, actuales.iterrows()):
        sufijo = "%" if fila["unidad"] == "%" else ""
        columna.metric(str(fila["serie"]), f"{fila['valor']:,.4f}{sufijo}")

    tabs = st.tabs(["Histórico tipo de cambio", "Tasas y SOFR", "Detalle descargable"])
    with tabs[0]:
        cambio = indicadores[indicadores["serie"].str.contains("cambio")]
        st.plotly_chart(px.line(cambio, x="fecha", y="valor", color="serie"), width="stretch")
    with tabs[1]:
        tasas = indicadores[~indicadores["serie"].str.contains("cambio")]
        st.plotly_chart(px.line(tasas, x="fecha", y="valor", color="serie"), width="stretch")
    with tabs[2]:
        st.dataframe(indicadores.tail(100), width="stretch", hide_index=True)
        st.download_button(
            "Descargar series sintéticas (.csv)",
            indicadores.to_csv(index=False).encode("utf-8"),
            "indicadores_sinteticos.csv",
            "text/csv",
        )


def render_vencimientos() -> None:
    st.title("Vencimientos, Fondeo y Covenants")
    datos = cargar_demo()
    pasivos = construir_maestro_pasivos(datos["pasivos.csv"])
    vencimientos = calendario_vencimientos(pasivos)
    lineas = uso_lineas(pasivos)
    covenants = datos["covenants.csv"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Compromisos", int(vencimientos["compromisos"].sum()))
    c2.metric("Línea disponible", _formato_moneda(float(lineas["linea_disponible"].sum())))
    c3.metric("Covenants por revisar", int(covenants["estatus"].eq("Revisar").sum()))

    tabs = st.tabs(["Calendario", "Líneas de fondeo", "Covenants", "Brecha de liquidez"])
    with tabs[0]:
        st.plotly_chart(px.bar(vencimientos, x="horizonte", y="total", color="moneda", barmode="group"), width="stretch")
        st.dataframe(vencimientos, width="stretch", hide_index=True)
    with tabs[1]:
        figura = px.bar(lineas, x="fondeador", y=["capital", "linea_disponible"], barmode="stack", title="Uso de líneas autorizadas")
        st.plotly_chart(figura, width="stretch")
        st.dataframe(lineas, width="stretch", hide_index=True)
    with tabs[2]:
        st.dataframe(covenants, width="stretch", hide_index=True)
    with tabs[3]:
        brecha = calcular_brecha_liquidez(datos["estados_financieros.csv"], pasivos)
        st.plotly_chart(px.bar(brecha, x="horizonte", y=["activos", "pasivos", "brecha"], barmode="group"), width="stretch")
        st.dataframe(brecha, width="stretch", hide_index=True)


def render_controles() -> None:
    st.title("Control y Trazabilidad")
    datos = cargar_demo()
    pasivos = construir_maestro_pasivos(datos["pasivos.csv"])
    cartera = construir_reporte_cartera(datos["cartera.csv"])
    conciliacion = conciliacion_reportada(datos["cifras_reportadas.csv"])
    controles = matriz_controles(datos["posicion_flujo.csv"], pasivos, cartera, conciliacion)
    c1, c2, c3 = st.columns(3)
    c1.metric("Reglas ejecutadas", len(controles))
    c2.metric("Controles correctos", int(controles["estatus"].eq("Correcto").sum()))
    c3.metric("Excepciones documentadas", int(controles["estatus"].ne("Correcto").sum()))
    tabs = st.tabs(["Matriz de controles", "Conciliación", "Trazabilidad"])
    with tabs[0]:
        st.dataframe(controles, width="stretch", hide_index=True)
    with tabs[1]:
        st.dataframe(conciliacion, width="stretch", hide_index=True)
    with tabs[2]:
        st.markdown(
            """
            **Linaje demostrativo:** insumo sintético → validación de esquema → homologación → cálculo →
            conciliación → reporte → bitácora. Cada salida puede rastrearse hasta un archivo y una etapa.
            """
        )
        st.dataframe(preparar_automates()["bitacora"], width="stretch", hide_index=True)
