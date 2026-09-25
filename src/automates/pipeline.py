from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from time import perf_counter
from uuid import uuid4

import pandas as pd

from .controls import (
    calendario_vencimientos,
    conciliacion_reportada,
    matriz_controles,
    resumen_ejecutivo,
    uso_lineas,
)
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


def _hash_archivo(ruta: Path) -> str:
    digest = sha256()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(65_536), b""):
            digest.update(bloque)
    return digest.hexdigest()


def _crear_manifiesto(directorio: Path) -> pd.DataFrame:
    filas = []
    for ruta in sorted(directorio.rglob("*.xlsx")):
        filas.append(
            {
                "archivo": ruta.relative_to(directorio).as_posix(),
                "bytes": ruta.stat().st_size,
                "sha256": _hash_archivo(ruta),
                "tipo": "Excel",
            }
        )
    return pd.DataFrame(filas)


def ejecutar_pipeline(directorio_datos: Path, directorio_salida: Path) -> dict[str, object]:
    directorio_salida.mkdir(parents=True, exist_ok=True)
    inicio = perf_counter()
    run_id = f"RUN-{uuid4().hex[:10].upper()}"
    eventos: list[dict[str, object]] = []

    def registrar(etapa: str, filas: int, archivo: str, detalle: str) -> None:
        eventos.append(
            {
                "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "run_id": run_id,
                "etapa": etapa,
                "estado": "Correcto",
                "filas": filas,
                "archivo": archivo,
                "detalle": detalle,
                "duracion_acumulada_ms": round((perf_counter() - inicio) * 1_000),
            }
        )

    estados = construir_estados_base(_cargar(directorio_datos, "estados_financieros.csv"))
    pasivos = construir_maestro_pasivos(_cargar(directorio_datos, "pasivos.csv"))
    cartera = construir_reporte_cartera(_cargar(directorio_datos, "cartera.csv"))
    brecha = calcular_brecha_liquidez(estados, pasivos)
    comparativo = comparativo_trazabilidad(cartera, cartera.copy(), "saldo_total")
    posiciones = _cargar(directorio_datos, "posicion_flujo.csv")
    covenants = _cargar(directorio_datos, "covenants.csv")
    conciliacion = conciliacion_reportada(_cargar(directorio_datos, "cifras_reportadas.csv"))
    vencimientos = calendario_vencimientos(pasivos)
    lineas = uso_lineas(pasivos)
    controles = matriz_controles(posiciones, pasivos, cartera, conciliacion)
    resumen = resumen_ejecutivo(posiciones, pasivos, cartera, covenants)

    tablas = {
        "estados_financieros_base.xlsx": estados,
        "maestro_pasivos_base.xlsx": pasivos,
        "reporte_cartera.xlsx": cartera,
        "brecha_liquidez.xlsx": brecha,
        "comparativo_trazabilidad.xlsx": comparativo,
        "conciliacion_reportada.xlsx": conciliacion,
        "matriz_controles.xlsx": controles,
        "calendario_vencimientos.xlsx": vencimientos,
        "uso_lineas_fondeo.xlsx": lineas,
        "seguimiento_covenants.xlsx": covenants,
        "resumen_ejecutivo.xlsx": resumen,
    }
    etiquetas = {
        "estados_financieros_base.xlsx": "Estados Financieros Base",
        "maestro_pasivos_base.xlsx": "Maestro de Pasivos Base",
        "reporte_cartera.xlsx": "Reporte de Cartera",
        "brecha_liquidez.xlsx": "Brecha de Liquidez",
        "comparativo_trazabilidad.xlsx": "Validación de trazabilidad",
        "conciliacion_reportada.xlsx": "Conciliación contra cifras reportadas",
        "matriz_controles.xlsx": "Matriz de controles",
        "calendario_vencimientos.xlsx": "Calendario de vencimientos",
        "uso_lineas_fondeo.xlsx": "Utilización de líneas",
        "seguimiento_covenants.xlsx": "Seguimiento de covenants",
        "resumen_ejecutivo.xlsx": "Resumen ejecutivo",
    }
    for archivo, tabla in tablas.items():
        tabla.to_excel(directorio_salida / archivo, index=False)
        registrar(etiquetas[archivo], len(tabla), archivo, "Transformación y exportación completadas")

    cantidad_reportes = generar_reportes_fondeadores(posiciones, directorio_salida / "reportes_fondeadores")
    registrar(
        "Reportería por fondeador",
        cantidad_reportes,
        "reportes_fondeadores/",
        "Tres entregables para cada uno de 13 fondeadores ficticios",
    )

    manifiesto = _crear_manifiesto(directorio_salida)
    manifiesto.to_csv(directorio_salida / "manifiesto_archivos.csv", index=False, encoding="utf-8")
    registrar(
        "Manifiesto de salida",
        len(manifiesto),
        "manifiesto_archivos.csv",
        "Inventario con tamaño y SHA-256 para comprobar integridad",
    )

    bitacora = pd.DataFrame(eventos)
    bitacora.to_csv(directorio_salida / "bitacora_ejecucion.csv", index=False, encoding="utf-8")
    return {
        "tablas": tablas,
        "bitacora": bitacora,
        "cantidad_reportes": cantidad_reportes,
        "manifiesto": manifiesto,
        "run_id": run_id,
        "directorio_salida": directorio_salida,
    }
