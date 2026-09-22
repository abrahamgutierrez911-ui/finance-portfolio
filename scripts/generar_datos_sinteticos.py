from pathlib import Path

import numpy as np
import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "data" / "synthetic"
RNG = np.random.default_rng(2027)


def posiciones_bancarias() -> pd.DataFrame:
    fechas = pd.date_range("2026-01-01", periods=120, freq="D")
    bancos = [f"Banco Demo {i:02d}" for i in range(1, 6)]
    fondeadores = [f"Fondeador Demo {i:02d}" for i in range(1, 14)]
    filas = []
    for fecha in fechas:
        for banco in bancos:
            inicial = float(RNG.integers(800_000, 5_000_000))
            entradas = float(RNG.integers(0, 900_000))
            salidas = float(RNG.integers(0, 750_000))
            filas.append(
                {
                    "fecha": fecha.date().isoformat(),
                    "banco": banco,
                    "fondeador": RNG.choice(fondeadores),
                    "saldo_inicial": inicial,
                    "entradas": entradas,
                    "salidas": salidas,
                    "saldo_final": inicial + entradas - salidas,
                    "dias_vencimiento": int(RNG.integers(1, 181)),
                }
            )
    return pd.DataFrame(filas)


def estados_financieros() -> pd.DataFrame:
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
            {"concepto": c, "tipo": t, "horizonte": h, "importe": float(RNG.integers(2_000_000, 25_000_000))}
            for c, t, h in conceptos
        ]
    )


def pasivos() -> pd.DataFrame:
    filas = []
    for i in range(1, 14):
        capital = float(RNG.integers(1_000_000, 9_000_000))
        interes = round(capital * float(RNG.uniform(0.01, 0.035)), 2)
        filas.append(
            {
                "fondeador": f"Fondeador Demo {i:02d}",
                "capital": capital,
                "interes": interes,
                "total": capital + interes,
                "linea_autorizada": float(RNG.integers(8_000_000, 18_000_000)),
                "dias_vencimiento": int(RNG.integers(15, 365)),
                "tasa_anual": round(float(RNG.uniform(0.10, 0.18)), 4),
            }
        )
    return pd.DataFrame(filas)


def cartera() -> pd.DataFrame:
    productos = ["Crédito simple", "Arrendamiento", "Factoraje"]
    filas = []
    for i in range(1, 121):
        capital = float(RNG.integers(80_000, 1_800_000))
        interes = round(capital * float(RNG.uniform(0.005, 0.03)), 2)
        dias_atraso = int(RNG.choice([0, 0, 0, 0, 15, 30, 60, 90]))
        filas.append(
            {
                "cliente": f"Cliente Demo {i:03d}",
                "producto": RNG.choice(productos),
                "capital_vigente": capital if dias_atraso == 0 else 0.0,
                "capital_vencido": capital if dias_atraso > 0 else 0.0,
                "interes": interes,
                "dias_atraso": dias_atraso,
                "garantia": RNG.choice(["Sí", "No"], p=[0.7, 0.3]),
            }
        )
    return pd.DataFrame(filas)


if __name__ == "__main__":
    SALIDA.mkdir(parents=True, exist_ok=True)
    conjuntos = {
        "posicion_flujo.csv": posiciones_bancarias(),
        "estados_financieros.csv": estados_financieros(),
        "pasivos.csv": pasivos(),
        "cartera.csv": cartera(),
    }
    for nombre, datos in conjuntos.items():
        datos.to_csv(SALIDA / nombre, index=False, encoding="utf-8")
        print(f"Creado {nombre}: {len(datos):,} filas")

