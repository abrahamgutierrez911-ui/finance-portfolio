from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def posiciones_bancarias(seed: int = 2027) -> pd.DataFrame:
    rng = _rng(seed)
    fechas = pd.date_range("2026-01-01", periods=180, freq="D")
    bancos = [f"Banco Demo {i:02d}" for i in range(1, 6)]
    fondeadores = [f"Fondeador Demo {i:02d}" for i in range(1, 14)]
    categorias = ["Cobranza", "Fondeo", "Operación", "Inversión"]
    empresas = ["Empresa Demo A", "Empresa Demo B"]
    monedas = ["MXN", "USD"]
    saldos = {
        (banco, empresa, moneda): float(rng.integers(800_000, 5_000_000))
        for banco in bancos
        for empresa in empresas
        for moneda in monedas
    }
    filas: list[dict[str, object]] = []
    operacion = 1
    for fecha in fechas:
        for banco in bancos:
            empresa = str(rng.choice(empresas))
            moneda = str(rng.choice(monedas, p=[0.85, 0.15]))
            llave = (banco, empresa, moneda)
            inicial = saldos[llave]
            entradas = float(rng.integers(25_000, 900_000))
            salidas = float(rng.integers(15_000, 750_000))
            final = inicial + entradas - salidas
            saldos[llave] = final
            filas.append(
                {
                    "operacion_id": f"OP-DEMO-{operacion:06d}",
                    "fecha": fecha.date().isoformat(),
                    "empresa": empresa,
                    "banco": banco,
                    "cuenta_demo": f"CTA-DEMO-{bancos.index(banco) + 1:02d}",
                    "moneda": moneda,
                    "categoria": str(rng.choice(categorias)),
                    "fondeador": str(rng.choice(fondeadores)),
                    "saldo_inicial": inicial,
                    "entradas": entradas,
                    "salidas": salidas,
                    "saldo_final": final,
                    "dias_vencimiento": int(rng.integers(1, 181)),
                }
            )
            operacion += 1
    return pd.DataFrame(filas)


def estados_financieros(seed: int = 2028) -> pd.DataFrame:
    rng = _rng(seed)
    conceptos = [
        ("Disponible", "Activo", "0-30 días"),
        ("Inversiones", "Activo", "0-30 días"),
        ("Cartera vigente", "Activo", "31-90 días"),
        ("Cartera vencida", "Activo", "91-180 días"),
        ("Otros activos", "Activo", "Más de 180 días"),
        ("Pasivos bursátiles", "Pasivo", "31-90 días"),
        ("Préstamos bancarios", "Pasivo", "91-180 días"),
        ("Otros pasivos", "Pasivo", "0-30 días"),
        ("Capital contable", "Capital", "Más de 180 días"),
    ]
    return pd.DataFrame(
        [
            {
                "concepto": concepto,
                "tipo": tipo,
                "horizonte": horizonte,
                "importe": float(rng.integers(2_000_000, 25_000_000)),
            }
            for concepto, tipo, horizonte in conceptos
        ]
    )


def pasivos(seed: int = 2029) -> pd.DataFrame:
    rng = _rng(seed)
    fecha_base = pd.Timestamp("2026-09-25")
    filas: list[dict[str, object]] = []
    for i in range(1, 14):
        capital = float(rng.integers(1_000_000, 9_000_000))
        interes = round(capital * float(rng.uniform(0.01, 0.035)), 2)
        dias = int(rng.integers(15, 365))
        filas.append(
            {
                "credito_id": f"CR-DEMO-{i:03d}",
                "fondeador": f"Fondeador Demo {i:02d}",
                "capital": capital,
                "interes": interes,
                "total": capital + interes,
                "linea_autorizada": float(rng.integers(9_000_000, 20_000_000)),
                "dias_vencimiento": dias,
                "fecha_vencimiento": (fecha_base + pd.Timedelta(days=dias)).date().isoformat(),
                "tasa_anual": round(float(rng.uniform(0.10, 0.18)), 4),
                "moneda": str(rng.choice(["MXN", "USD"], p=[0.8, 0.2])),
            }
        )
    return pd.DataFrame(filas)


def cartera(seed: int = 2030) -> pd.DataFrame:
    rng = _rng(seed)
    productos = ["Crédito simple", "Arrendamiento", "Factoraje"]
    filas: list[dict[str, object]] = []
    for i in range(1, 121):
        capital = float(rng.integers(80_000, 1_800_000))
        interes = round(capital * float(rng.uniform(0.005, 0.03)), 2)
        dias_atraso = int(rng.choice([0, 0, 0, 0, 15, 30, 60, 90]))
        filas.append(
            {
                "contrato_id": f"CT-DEMO-{i:04d}",
                "cliente": f"Cliente Demo {i:03d}",
                "producto": str(rng.choice(productos)),
                "capital_vigente": capital if dias_atraso == 0 else 0.0,
                "capital_vencido": capital if dias_atraso > 0 else 0.0,
                "interes": interes,
                "dias_atraso": dias_atraso,
                "garantia": str(rng.choice(["Sí", "No"], p=[0.7, 0.3])),
                "region": str(rng.choice(["Centro", "Norte", "Occidente", "Sureste"])),
            }
        )
    return pd.DataFrame(filas)


def indicadores_economicos(seed: int = 2031) -> pd.DataFrame:
    rng = _rng(seed)
    fechas = pd.bdate_range("2025-09-25", "2026-09-25")
    configuracion = {
        "Tipo de cambio FIX demo": (17.75, 0.055, "Fuente pública simulada", "MXN/USD"),
        "Tipo de cambio diario demo": (17.70, 0.06, "Fuente pública simulada", "MXN/USD"),
        "SOFR demo": (3.88, 0.025, "Fuente pública simulada", "%"),
        "Tasa objetivo demo": (6.50, 0.012, "Fuente pública simulada", "%"),
    }
    filas: list[dict[str, object]] = []
    for serie, (inicio, volatilidad, fuente, unidad) in configuracion.items():
        valores = inicio + np.cumsum(rng.normal(0, volatilidad, len(fechas)))
        if unidad == "%":
            valores = np.clip(valores, 0.1, None)
        for fecha, valor in zip(fechas, valores):
            filas.append(
                {
                    "fecha": fecha.date().isoformat(),
                    "serie": serie,
                    "valor": round(float(valor), 6),
                    "unidad": unidad,
                    "fuente": fuente,
                    "es_simulado": True,
                }
            )
    return pd.DataFrame(filas)


def covenants(seed: int = 2032) -> pd.DataFrame:
    rng = _rng(seed)
    reglas = [
        ("Liquidez mínima", ">=", 1.00, "x"),
        ("Cartera vencida máxima", "<=", 0.18, "%"),
        ("Apalancamiento máximo", "<=", 4.00, "x"),
        ("Cobertura de deuda", ">=", 1.15, "x"),
    ]
    filas: list[dict[str, object]] = []
    for i, (regla, operador, limite, unidad) in enumerate(reglas, 1):
        actual = limite + float(rng.uniform(-0.22, 0.28))
        cumple = actual >= limite if operador == ">=" else actual <= limite
        filas.append(
            {
                "covenant_id": f"CV-DEMO-{i:02d}",
                "regla": regla,
                "operador": operador,
                "limite": limite,
                "valor_actual": round(actual, 4),
                "unidad": unidad,
                "periodicidad": "Mensual",
                "estatus": "Cumple" if cumple else "Revisar",
                "responsable": "Tesorería Demo",
            }
        )
    return pd.DataFrame(filas)


def cifras_reportadas(estados: pd.DataFrame, pasivos_df: pd.DataFrame, cartera_df: pd.DataFrame) -> pd.DataFrame:
    activo = float(estados.loc[estados["tipo"].eq("Activo"), "importe"].sum())
    pasivo = float(pasivos_df["total"].sum())
    cartera_total = float(
        (cartera_df["capital_vigente"] + cartera_df["capital_vencido"] + cartera_df["interes"]).sum()
    )
    return pd.DataFrame(
        [
            {"concepto": "Activo total", "fuente_operativa": activo, "cifra_reportada": activo, "tolerancia": 1.0},
            {"concepto": "Pasivo financiero", "fuente_operativa": pasivo, "cifra_reportada": pasivo + 2_500.0, "tolerancia": 5_000.0},
            {"concepto": "Cartera total", "fuente_operativa": cartera_total, "cifra_reportada": cartera_total - 7_500.0, "tolerancia": 5_000.0},
        ]
    )


def generar_datasets(seed: int = 2027) -> dict[str, pd.DataFrame]:
    estados = estados_financieros(seed + 1)
    pasivos_df = pasivos(seed + 2)
    cartera_df = cartera(seed + 3)
    return {
        "posicion_flujo.csv": posiciones_bancarias(seed),
        "estados_financieros.csv": estados,
        "pasivos.csv": pasivos_df,
        "cartera.csv": cartera_df,
        "indicadores_economicos.csv": indicadores_economicos(seed + 4),
        "covenants.csv": covenants(seed + 5),
        "cifras_reportadas.csv": cifras_reportadas(estados, pasivos_df, cartera_df),
    }


def guardar_datasets(directorio: Path, seed: int = 2027) -> dict[str, int]:
    directorio.mkdir(parents=True, exist_ok=True)
    conteos: dict[str, int] = {}
    for nombre, datos in generar_datasets(seed).items():
        datos.to_csv(directorio / nombre, index=False, encoding="utf-8")
        conteos[nombre] = len(datos)
    return conteos
