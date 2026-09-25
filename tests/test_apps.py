from pathlib import Path

from streamlit.testing.v1 import AppTest


RAIZ = Path(__file__).resolve().parents[1]


def test_portafolio_carga_las_tres_vistas() -> None:
    app = AppTest.from_file(str(RAIZ / "streamlit_app.py"), default_timeout=30).run()
    assert not app.exception
    assert app.title[0].value == "Portafolio de Datos, BI y Tesorería"

    app.radio[0].set_value("AutomaTES").run(timeout=30)
    assert not app.exception
    assert app.title[0].value.startswith("AutomaTES")
    assert any(m.label == "Reportes por fondeador" and m.value == "39" for m in app.metric)

    app.radio[0].set_value("Dashboard").run(timeout=30)
    assert not app.exception
    assert app.title[0].value == "Dashboard de Tesorería y Fondeo"
    assert [tab.label for tab in app.tabs] == ["Posición bancaria", "Brecha de liquidez", "Pasivos", "Cartera"]
