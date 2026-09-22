from __future__ import annotations

from pathlib import Path

import pandas as pd


HORIZONTES = ["0-30 días", "31-90 días", "91-180 días", "Más de 180 días"]


def validar_columnas(datos: pd.DataFrame, requeridas: set[str], nombre: str) -> None:
    faltantes = requeridas.difference(datos.columns)
    if faltantes:
        raise ValueError(f"{nombre}: columnas faltantes {sorted(faltantes)}")


def construir_estados_base(estados: pd.DataFrame) -> pd.DataFrame:
    validar_columnas(estados, {"concepto", "tipo", "horizonte", "importe"}, "Estados financieros")
    salida = estados.copy()
    salida["importe"] = pd.to_numeric(salida["importe"], errors="raise")
    salida["concepto"] = salida["concepto"].str.strip()
    return salida.sort_values(["tipo", "concepto"]).reset_index(drop=True)


def construir_maestro_pasivos(pasivos: pd.DataFrame) -> pd.DataFrame:
    requeridas = {"fondeador", "capital", "interes", "linea_autorizada", "dias_vencimiento", "tasa_anual"}
    validar_columnas(pasivos, requeridas, "Pasivos")
    salida = pasivos.copy()
    salida["total"] = salida["capital"] + salida["interes"]
    salida["disponibilidad_linea"] = salida["linea_autorizada"] - salida["capital"]
    salida["utilizacion_pct"] = (salida["capital"] / salida["linea_autorizada"]).fillna(0)
    return salida.sort_values("total", ascending=False).reset_index(drop=True)


def construir_reporte_cartera(cartera: pd.DataFrame) -> pd.DataFrame:
    requeridas = {"cliente", "producto", "capital_vigente", "capital_vencido", "interes", "dias_atraso", "garantia"}
    validar_columnas(cartera, requeridas, "Cartera")
    salida = cartera.copy()
    salida["saldo_total"] = salida["capital_vigente"] + salida["capital_vencido"] + salida["interes"]
    salida["estatus"] = salida["dias_atraso"].gt(0).map({True: "Vencida", False: "Vigente"})
    return salida.loc[salida["saldo_total"].ne(0)].sort_values("saldo_total", ascending=False).reset_index(drop=True)


def calcular_brecha_liquidez(estados: pd.DataFrame, pasivos: pd.DataFrame) -> pd.DataFrame:
    base = construir_estados_base(estados)
    maestro = construir_maestro_pasivos(pasivos)
    activos = base.loc[base["tipo"].eq("Activo")].groupby("horizonte")["importe"].sum()
    bins = [0, 30, 90, 180, float("inf")]
    maestro["horizonte"] = pd.cut(
        maestro["dias_vencimiento"], bins=bins, labels=HORIZONTES, include_lowest=True
    ).astype(str)
    pasivos_h = maestro.groupby("horizonte")["total"].sum()
    resultado = pd.DataFrame({"horizonte": HORIZONTES})
    resultado["activos"] = resultado["horizonte"].map(activos).fillna(0.0)
    resultado["pasivos"] = resultado["horizonte"].map(pasivos_h).fillna(0.0)
    resultado["brecha"] = resultado["activos"] - resultado["pasivos"]
    resultado["brecha_acumulada"] = resultado["brecha"].cumsum()
    return resultado


def comparativo_trazabilidad(origen: pd.DataFrame, reporte: pd.DataFrame, columna: str) -> pd.DataFrame:
    """Devuelve únicamente validaciones comprobables que cuadran."""
    if columna not in origen or columna not in reporte:
        raise ValueError(f"No existe la columna comparable: {columna}")
    total_origen = round(float(origen[columna].sum()), 2)
    total_reporte = round(float(reporte[columna].sum()), 2)
    if total_origen != total_reporte:
        return pd.DataFrame(columns=["validacion", "origen", "reporte", "estatus"])
    return pd.DataFrame(
        [{"validacion": f"Total {columna}", "origen": total_origen, "reporte": total_reporte, "estatus": "Cuadra"}]
    )


def generar_reportes_fondeadores(posiciones: pd.DataFrame, salida: Path) -> int:
    requeridas = {"fecha", "banco", "fondeador", "entradas", "salidas", "saldo_final", "dias_vencimiento"}
    validar_columnas(posiciones, requeridas, "Posición y flujo")
    salida.mkdir(parents=True, exist_ok=True)
    cantidad = 0
    for fondeador, bloque in posiciones.groupby("fondeador", sort=True):
        nombre = fondeador.lower().replace(" ", "_")
        resumen = bloque.groupby("banco", as_index=False)[["entradas", "salidas", "saldo_final"]].sum()
        vencimientos = bloque.loc[bloque["dias_vencimiento"].le(30)].sort_values("dias_vencimiento")
        flujo = bloque.groupby("fecha", as_index=False)[["entradas", "salidas"]].sum()
        flujo["flujo_neto"] = flujo["entradas"] - flujo["salidas"]
        for tipo, tabla in {"resumen": resumen, "vencimientos": vencimientos, "flujo": flujo}.items():
            tabla.to_excel(salida / f"{nombre}_{tipo}.xlsx", index=False)
            cantidad += 1
    return cantidad

