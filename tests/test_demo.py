from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from automates.demo_data import generar_datasets, guardar_datasets  # noqa: E402
from automates.pipeline import ejecutar_pipeline  # noqa: E402


def test_datos_sinteticos_son_reproducibles() -> None:
    primero = generar_datasets(2027)
    segundo = generar_datasets(2027)
    assert primero.keys() == segundo.keys()
    for nombre in primero:
        assert primero[nombre].equals(segundo[nombre])


def test_pipeline_completo_genera_entregables_y_bitacora(tmp_path: Path) -> None:
    datos = tmp_path / "datos"
    salida = tmp_path / "salida"
    guardar_datasets(datos)
    resultado = ejecutar_pipeline(datos, salida)

    assert resultado["cantidad_reportes"] == 39
    assert len(list((salida / "reportes_fondeadores").glob("*.xlsx"))) == 39
    assert len(list(salida.glob("*.xlsx"))) == 5
    assert (salida / "bitacora_ejecucion.csv").exists()
    assert set(resultado["bitacora"]["estado"]) == {"Correcto"}


def test_datos_no_contienen_entidades_reales() -> None:
    datasets = generar_datasets()
    posiciones = datasets["posicion_flujo.csv"]
    pasivos = datasets["pasivos.csv"]
    cartera = datasets["cartera.csv"]
    assert posiciones["banco"].str.match(r"Banco Demo \d{2}").all()
    assert posiciones["fondeador"].str.match(r"Fondeador Demo \d{2}").all()
    assert pasivos["fondeador"].str.match(r"Fondeador Demo \d{2}").all()
    assert cartera["cliente"].str.match(r"Cliente Demo \d{3}").all()
