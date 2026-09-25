from pathlib import Path
import sys

import pytest


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from automates.controls import calendario_vencimientos, conciliacion_reportada, matriz_controles, uso_lineas
from automates.core import construir_maestro_pasivos, construir_reporte_cartera
from automates.demo_data import generar_datasets


def test_conciliacion_aplica_tolerancias_y_documenta_excepcion() -> None:
    datos = generar_datasets()
    conciliacion = conciliacion_reportada(datos["cifras_reportadas.csv"])
    assert conciliacion["estatus"].tolist() == ["Cuadra", "Cuadra", "Revisar"]
    assert conciliacion.loc[conciliacion["estatus"].eq("Revisar"), "diferencia_abs"].iloc[0] == 7_500.0


def test_matriz_controles_valida_integridad_calculos_y_limites() -> None:
    datos = generar_datasets()
    pasivos = construir_maestro_pasivos(datos["pasivos.csv"])
    cartera = construir_reporte_cartera(datos["cartera.csv"])
    conciliacion = conciliacion_reportada(datos["cifras_reportadas.csv"])
    controles = matriz_controles(datos["posicion_flujo.csv"], pasivos, cartera, conciliacion)
    assert len(controles) == 8
    assert controles.loc[controles["severidad"].eq("Crítico"), "estatus"].eq("Correcto").all()
    assert controles["estatus"].isin(["Correcto", "Revisar", "Monitorear"]).all()


def test_vencimientos_y_lineas_conservan_totales() -> None:
    pasivos = construir_maestro_pasivos(generar_datasets()["pasivos.csv"])
    vencimientos = calendario_vencimientos(pasivos)
    lineas = uso_lineas(pasivos)
    assert vencimientos["total"].sum() == pytest.approx(pasivos["total"].sum())
    assert (lineas["capital"] + lineas["linea_disponible"]).sum() == pytest.approx(
        lineas["linea_autorizada"].sum()
    )
