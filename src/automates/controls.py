from __future__ import annotations

import pandas as pd

from .core import HORIZONTES


def conciliacion_reportada(cifras: pd.DataFrame) -> pd.DataFrame:
    requeridas = {"concepto", "fuente_operativa", "cifra_reportada", "tolerancia"}
    faltantes = requeridas.difference(cifras.columns)
    if faltantes:
        raise ValueError(f"Cifras reportadas: columnas faltantes {sorted(faltantes)}")
    salida = cifras.copy()
    salida["diferencia"] = salida["fuente_operativa"] - salida["cifra_reportada"]
    salida["diferencia_abs"] = salida["diferencia"].abs()
    salida["estatus"] = salida.apply(
        lambda fila: "Cuadra" if fila["diferencia_abs"] <= fila["tolerancia"] else "Revisar", axis=1
    )
    return salida


def calendario_vencimientos(pasivos: pd.DataFrame) -> pd.DataFrame:
    salida = pasivos.copy()
    bins = [0, 30, 90, 180, float("inf")]
    salida["horizonte"] = pd.cut(
        salida["dias_vencimiento"], bins=bins, labels=HORIZONTES, include_lowest=True
    ).astype(str)
    return (
        salida.groupby(["horizonte", "moneda"], observed=False, as_index=False)
        .agg(capital=("capital", "sum"), intereses=("interes", "sum"), compromisos=("credito_id", "count"))
        .assign(total=lambda x: x["capital"] + x["intereses"])
    )


def uso_lineas(pasivos: pd.DataFrame) -> pd.DataFrame:
    columnas = ["fondeador", "moneda", "capital", "linea_autorizada", "fecha_vencimiento", "tasa_anual"]
    salida = pasivos[columnas].copy()
    salida["linea_disponible"] = salida["linea_autorizada"] - salida["capital"]
    salida["utilizacion_pct"] = salida["capital"] / salida["linea_autorizada"]
    salida["nivel"] = pd.cut(
        salida["utilizacion_pct"],
        bins=[-float("inf"), 0.70, 0.90, float("inf")],
        labels=["Disponible", "Atención", "Alta utilización"],
    ).astype(str)
    return salida.sort_values("utilizacion_pct", ascending=False).reset_index(drop=True)


def matriz_controles(
    posiciones: pd.DataFrame,
    pasivos: pd.DataFrame,
    cartera: pd.DataFrame,
    conciliacion: pd.DataFrame,
) -> pd.DataFrame:
    diferencia_saldos = (
        posiciones["saldo_inicial"] + posiciones["entradas"] - posiciones["salidas"] - posiciones["saldo_final"]
    ).abs()
    diferencia_pasivos = (pasivos["capital"] + pasivos["interes"] - pasivos["total"]).abs()
    controles = [
        ("Integridad", "IDs de movimiento únicos", posiciones["operacion_id"].duplicated().sum(), 0, "Crítico"),
        ("Integridad", "Contratos de cartera únicos", cartera["contrato_id"].duplicated().sum(), 0, "Crítico"),
        ("Calidad", "Campos obligatorios vacíos", int(posiciones.isna().sum().sum()), 0, "Crítico"),
        ("Cálculo", "Diferencias en ecuación de saldo", int(diferencia_saldos.gt(0.01).sum()), 0, "Crítico"),
        ("Cálculo", "Diferencias en total de pasivos", int(diferencia_pasivos.gt(0.01).sum()), 0, "Crítico"),
        ("Límites", "Líneas con capital mayor al autorizado", int((pasivos["capital"] > pasivos["linea_autorizada"]).sum()), 0, "Crítico"),
        ("Trazabilidad", "Conciliaciones fuera de tolerancia", int(conciliacion["estatus"].eq("Revisar").sum()), 0, "Advertencia"),
        ("Riesgo", "Contratos con más de 60 días de atraso", int(cartera["dias_atraso"].gt(60).sum()), 0, "Informativo"),
    ]
    filas: list[dict[str, object]] = []
    for modulo, control, incidencias, esperado, severidad in controles:
        estatus = "Correcto" if incidencias == esperado else ("Revisar" if severidad != "Informativo" else "Monitorear")
        filas.append(
            {
                "modulo": modulo,
                "control": control,
                "resultado": incidencias,
                "esperado": esperado,
                "severidad": severidad,
                "estatus": estatus,
            }
        )
    return pd.DataFrame(filas)


def resumen_ejecutivo(
    posiciones: pd.DataFrame,
    pasivos: pd.DataFrame,
    cartera: pd.DataFrame,
    covenants: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"indicador": "Entradas acumuladas", "valor": float(posiciones["entradas"].sum()), "unidad": "MXN demo"},
            {"indicador": "Salidas acumuladas", "valor": float(posiciones["salidas"].sum()), "unidad": "MXN demo"},
            {"indicador": "Pasivo financiero", "valor": float(pasivos["total"].sum()), "unidad": "MXN demo"},
            {"indicador": "Cartera total", "valor": float(cartera["saldo_total"].sum()), "unidad": "MXN demo"},
            {"indicador": "Cartera vencida", "valor": float(cartera.loc[cartera["estatus"].eq("Vencida"), "saldo_total"].sum()), "unidad": "MXN demo"},
            {"indicador": "Covenants por revisar", "valor": int(covenants["estatus"].eq("Revisar").sum()), "unidad": "controles"},
        ]
    )
