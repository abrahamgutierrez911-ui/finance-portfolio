from pathlib import Path

from streamlit.testing.v1 import AppTest


RAIZ = Path(__file__).resolve().parents[1]


def test_portafolio_carga_los_modulos_principales() -> None:
    app = AppTest.from_file(str(RAIZ / "streamlit_app.py"), default_timeout=30).run()
    assert not app.exception
    assert app.title[0].value == "Portafolio de Datos, BI y Tesorería"

    app.radio[0].set_value("Centro de reportes").run(timeout=30)
    assert not app.exception
    assert app.title[0].value.startswith("Centro de reportes")
    assert any(m.label == "Reportes por fondeador" and m.value == "39" for m in app.metric)
    assert any(m.label == "Archivos descargables" and m.value == "52" for m in app.metric)

    app.radio[0].set_value("Posición bancaria").run(timeout=30)
    assert not app.exception
    assert app.title[0].value == "Dashboard de Posición Bancaria"
    assert [tab.label for tab in app.tabs] == ["Movimientos", "Gráficas", "Comparativo", "Validación"]

    app.radio[0].set_value("Indicadores económicos").run(timeout=30)
    assert not app.exception
    assert app.title[0].value == "Indicadores Económicos"

    app.radio[0].set_value("Vencimientos y fondeo").run(timeout=30)
    assert not app.exception
    assert app.title[0].value == "Vencimientos, Fondeo y Covenants"

    app.radio[0].set_value("Control y trazabilidad").run(timeout=30)
    assert not app.exception
    assert app.title[0].value == "Control y Trazabilidad"
