# Dashboard de posición, flujo bancario y liquidez

## Objetivo

Centralizar en una sola vista la posición bancaria y los flujos de efectivo para facilitar el seguimiento de liquidez, cartera, pasivos y fondeo.

## Cómo verlo

```bash
streamlit run dashboard/app.py
```

No requiere bases externas: los datos se crean en memoria a partir del generador sintético del repositorio.

## Vistas interactivas

- **Posición bancaria:** entradas, salidas, flujo neto, saldo final y filtro por banco.
- **Brecha de liquidez:** activos, pasivos, brecha y acumulado por horizonte.
- **Pasivos:** capital, intereses, total, disponibilidad y utilización de línea.
- **Cartera:** producto, estatus, saldo, atraso y garantía ficticia.

## Tecnologías

- Python y pandas para preparación y agregación.
- Streamlit para la interfaz.
- Plotly para visualizaciones interactivas.
- Datos sintéticos reproducibles mediante NumPy.

## Privacidad

La aplicación usa únicamente `Banco Demo`, `Fondeador Demo` y `Cliente Demo`. No contiene números de cuenta, CLABE, beneficiarios, saldos, fechas o instituciones reales.
