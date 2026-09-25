# Dashboard de posición, flujo bancario y liquidez

## Objetivo

Centralizar en una sola vista la posición bancaria y los flujos de efectivo para facilitar el seguimiento de liquidez, cartera, pasivos y fondeo.

## Cómo verlo

```bash
streamlit run dashboard/app.py
```

No requiere bases externas: los datos se crean en memoria a partir del generador sintético del repositorio.

## Módulos interactivos

- **Centro de reportes:** insumos, pasos, entregables, controles, conciliación y bitácora.
- **Posición bancaria:** entradas, salidas, flujo neto y filtros por empresa, banco, moneda y categoría.
- **Indicadores económicos:** históricos offline simulados de tipo de cambio y tasas.
- **Vencimientos:** compromisos por horizonte y moneda, más brecha de liquidez.
- **Fondeo y covenants:** utilización de líneas, disponibilidad y seguimiento de reglas.
- **Control y trazabilidad:** excepciones documentadas y linaje de los resultados.

## Tecnologías

- Python y pandas para preparación y agregación.
- Streamlit para la interfaz.
- Plotly para visualizaciones interactivas.
- Datos sintéticos reproducibles mediante NumPy.

## Privacidad

La aplicación usa únicamente `Banco Demo`, `Fondeador Demo` y `Cliente Demo`. No contiene números de cuenta, CLABE, beneficiarios, saldos, fechas o instituciones reales.
