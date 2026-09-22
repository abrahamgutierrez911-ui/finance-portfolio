from pathlib import Path
import sys

import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from automates.core import (  # noqa: E402
    calcular_brecha_liquidez,
    comparativo_trazabilidad,
    construir_estados_base,
    construir_maestro_pasivos,
    construir_reporte_cartera,
    generar_reportes_fondeadores,
)


def cargar(nombre: str) -> pd.DataFrame:
    return pd.read_csv(RAIZ / "data" / "synthetic" / nombre)


if __name__ == "__main__":
    salida = RAIZ / "output"
    salida.mkdir(exist_ok=True)
    estados = construir_estados_base(cargar("estados_financieros.csv"))
    pasivos = construir_maestro_pasivos(cargar("pasivos.csv"))
    cartera = construir_reporte_cartera(cargar("cartera.csv"))
    brecha = calcular_brecha_liquidez(estados, pasivos)
    estados.to_excel(salida / "estados_financieros_base.xlsx", index=False)
    pasivos.to_excel(salida / "maestro_pasivos_base.xlsx", index=False)
    cartera.to_excel(salida / "reporte_cartera.xlsx", index=False)
    brecha.to_excel(salida / "brecha_liquidez.xlsx", index=False)
    comparativo = comparativo_trazabilidad(cartera, cartera.copy(), "saldo_total")
    comparativo.to_excel(salida / "comparativo_trazabilidad.xlsx", index=False)
    posiciones = cargar("posicion_flujo.csv")
    cantidad = generar_reportes_fondeadores(posiciones, salida / "reportes_fondeadores")
    print(f"Pipeline completado. Reportes por fondeador: {cantidad}")

