from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def posiciones_bancarias(seed: int = 2027) -> pd.DataFrame:
    rng = _rng(seed)
    fechas = pd.date_range("2026-01-01", periods=120, freq="D")
    bancos = [f"Banco Demo {i:02d}" for i in range(1, 6)]
    fondeadores = [f"Fondeador Demo {i:02d}" for i in range(1, 14)]
    filas: list[dict[str, object]] = []
    for fecha in fechas:
        for banco in bancos:
            inicial = float(rng.integers(800_000, 5_000_000))
            entradas = float(rng.integers(0, 900_000))
            salidas = float(rng.integers(0, 750_000))
            filas.append(
                {
                    "fecha": fecha.date().isoformat(),
                    "banco": banco,
                    "fondeador": rng.choice(fondeadores),
                    "saldo_inicial": inicial,
                    "entradas": entradas,
                    "salidas": salidas,
                    "saldo_final": inicial + entradas - salidas,
                    "dias_vencimiento": int(rng.integers(1, 181)),
                }
            )
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
    filas: list[dict[str, object]] = []
    for i in range(1, 14):
        capital = float(rng.integers(1_000_000, 9_000_000))
        interes = round(capital * float(rng.uniform(0.01, 0.035)), 2)
        filas.append(
            {
                "fondeador": f"Fondeador Demo {i:02d}",
                "capital": capital,
                "interes": interes,
                "total": capital + interes,
                "linea_autorizada": float(rng.integers(8_000_000, 18_000_000)),
                "dias_vencimiento": int(rng.integers(15, 365)),
                "tasa_anual": round(float(rng.uniform(0.10, 0.18)), 4),
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
                "cliente": f"Cliente Demo {i:03d}",
                "producto": rng.choice(productos),
                "capital_vigente": capital if dias_atraso == 0 else 0.0,
                "capital_vencido": capital if dias_atraso > 0 else 0.0,
                "interes": interes,
                "dias_atraso": dias_atraso,
                "garantia": rng.choice(["Sí", "No"], p=[0.7, 0.3]),
            }
        )
    return pd.DataFrame(filas)


def generar_datasets(seed: int = 2027) -> dict[str, pd.DataFrame]:
    return {
        "posicion_flujo.csv": posiciones_bancarias(seed),
        "estados_financieros.csv": estados_financieros(seed + 1),
        "pasivos.csv": pasivos(seed + 2),
        "cartera.csv": cartera(seed + 3),
    }


def guardar_datasets(directorio: Path, seed: int = 2027) -> dict[str, int]:
    directorio.mkdir(parents=True, exist_ok=True)
    conteos: dict[str, int] = {}
    for nombre, datos in generar_datasets(seed).items():
        datos.to_csv(directorio / nombre, index=False, encoding="utf-8")
        conteos[nombre] = len(datos)
    return conteos
