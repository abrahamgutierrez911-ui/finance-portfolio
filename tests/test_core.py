from pathlib import Path
import sys

import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from automates.core import comparativo_trazabilidad, construir_maestro_pasivos, construir_reporte_cartera, generar_reportes_fondeadores  # noqa: E402


def test_maestro_pasivos_calcula_totales() -> None:
    base = pd.DataFrame([{"fondeador": "Demo", "capital": 100.0, "interes": 10.0, "linea_autorizada": 200.0, "dias_vencimiento": 30, "tasa_anual": 0.12}])
    resultado = construir_maestro_pasivos(base)
    assert resultado.loc[0, "total"] == 110.0
    assert resultado.loc[0, "disponibilidad_linea"] == 100.0


def test_cartera_excluye_saldos_cero() -> None:
    base = pd.DataFrame([
        {"cliente": "A", "producto": "Crédito", "capital_vigente": 100.0, "capital_vencido": 0.0, "interes": 5.0, "dias_atraso": 0, "garantia": "Sí"},
        {"cliente": "B", "producto": "Crédito", "capital_vigente": 0.0, "capital_vencido": 0.0, "interes": 0.0, "dias_atraso": 0, "garantia": "No"},
    ])
    assert construir_reporte_cartera(base)["cliente"].tolist() == ["A"]


def test_comparativo_solo_muestra_validaciones_que_cuadran() -> None:
    origen = pd.DataFrame({"total": [100.0, 50.0]})
    assert comparativo_trazabilidad(origen, origen.copy(), "total").loc[0, "estatus"] == "Cuadra"
    assert comparativo_trazabilidad(origen, pd.DataFrame({"total": [149.0]}), "total").empty


def test_genera_39_reportes(tmp_path: Path) -> None:
    filas = [
        {"fecha": "2026-01-01", "banco": "Banco Demo", "fondeador": f"Fondeador Demo {i:02d}", "entradas": 10.0, "salidas": 5.0, "saldo_final": 100.0, "dias_vencimiento": 10}
        for i in range(1, 14)
    ]
    total = generar_reportes_fondeadores(pd.DataFrame(filas), tmp_path)
    assert total == 39
    assert len(list(tmp_path.glob("*.xlsx"))) == 39

