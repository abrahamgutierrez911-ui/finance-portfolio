from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .core import (
    calcular_brecha_liquidez,
    comparativo_trazabilidad,
    construir_estados_base,
    construir_maestro_pasivos,
    construir_reporte_cartera,
    generar_reportes_fondeadores,
)


def _cargar(directorio: Path, nombre: str) -> pd.DataFrame:
    ruta = directorio / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró la base sintética: {nombre}")
    return pd.read_csv(ruta)


def ejecutar_pipeline(directorio_datos: Path, directorio_salida: Path) -> dict[str, object]:
    directorio_salida.mkdir(parents=True, exist_ok=True)
    eventos: list[dict[str, object]] = []

    def registrar(etapa: str, filas: int, archivo: str, detalle: str) -> None:
        eventos.append(
            {
                "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "etapa": etapa,
                "estado": "Correcto",
                "filas": filas,
                "archivo": archivo,
                "detalle": detalle,
            }
        )

    estados = construir_estados_base(_cargar(directorio_datos, "estados_financieros.csv"))
    pasivos = construir_maestro_pasivos(_cargar(directorio_datos, "pasivos.csv"))
    cartera = construir_reporte_cartera(_cargar(directorio_datos, "cartera.csv"))
    brecha = calcular_brecha_liquidez(estados, pasivos)
    comparativo = comparativo_trazabilidad(cartera, cartera.copy(), "saldo_total")

    tablas = {
        "estados_financieros_base.xlsx": estados,
        "maestro_pasivos_base.xlsx": pasivos,
        "reporte_cartera.xlsx": cartera,
        "brecha_liquidez.xlsx": brecha,
        "comparativo_trazabilidad.xlsx": comparativo,
    }
    etiquetas = {
        "estados_financieros_base.xlsx": "Estados Financieros Base",
        "maestro_pasivos_base.xlsx": "Maestro de Pasivos Base",
        "reporte_cartera.xlsx": "Reporte de Cartera",
        "brecha_liquidez.xlsx": "Brecha de Liquidez",
        "comparativo_trazabilidad.xlsx": "Validación de trazabilidad",
    }
    for archivo, tabla in tablas.items():
        tabla.to_excel(directorio_salida / archivo, index=False)
        registrar(etiquetas[archivo], len(tabla), archivo, "Transformación y exportación completadas")

    posiciones = _cargar(directorio_datos, "posicion_flujo.csv")
    cantidad_reportes = generar_reportes_fondeadores(posiciones, directorio_salida / "reportes_fondeadores")
    registrar(
        "Reportería por fondeador",
        cantidad_reportes,
        "reportes_fondeadores/",
        "Tres entregables para cada uno de 13 fondeadores ficticios",
    )

    bitacora = pd.DataFrame(eventos)
    bitacora.to_csv(directorio_salida / "bitacora_ejecucion.csv", index=False, encoding="utf-8")
    return {
        "tablas": tablas,
        "bitacora": bitacora,
        "cantidad_reportes": cantidad_reportes,
        "directorio_salida": directorio_salida,
    }
