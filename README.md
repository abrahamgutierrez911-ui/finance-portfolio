# Abraham Ramsés Gutiérrez Valdés

## Analista de Datos | Business Intelligence | Tesorería

Economista egresado con experiencia en automatización de reportes financieros, análisis de datos, procesos ETL y dashboards. Trabajo con Python, pandas, SQL, Power BI, Excel avanzado y Odoo ERP para transformar procesos manuales en soluciones reproducibles y trazables.

> Portafolio basado en proyectos desarrollados profesionalmente. Las versiones públicas fueron reconstruidas desde cero con datos sintéticos y lógica demostrativa: no contienen bases, clientes, cuentas, contratos, saldos, documentos ni código interno de ningún empleador.

## Resultados destacados

- Automatización aproximada de 39 reportes financieros: un promedio de tres reportes para cada uno de 13 fondeadores.
- Reducción del procesamiento total de una o dos semanas a dos o tres días.
- Reducción aproximada del 75% en el tiempo dedicado a transformación de datos, generación de reportes y consulta de información.
- Centralización de posición y flujo bancario mediante dashboards e indicadores financieros.

## Proyectos

### 1. AutomaTES - Automatización de reportes financieros

Caso de estudio derivado de un proyecto real de Tesorería y Fondeo. La reconstrucción pública procesa estados financieros, pasivos, cartera, vencimientos y flujos; valida trazabilidad y genera información ficticia para 13 fondeadores con tres entregables por cada uno.

**Tecnologías:** Python, pandas, openpyxl, Excel y procesos ETL.

**Demuestra:**

- Estados Financieros Base.
- Maestro de Pasivos Base.
- Brecha de Liquidez.
- Reporte de Cartera.
- Comparativo de Trazabilidad.
- Reporterías por fondeador.
- Validación, bitácoras y exportación a Excel.

[Consultar el caso de estudio](projects/automatizacion-reportes/README.md)

### 2. Dashboard de posición, flujo bancario y liquidez

Dashboard demostrativo basado en el proyecto profesional para visualizar saldos, entradas, salidas, flujo neto, posición bancaria, estructura de pasivos, cartera y brecha de liquidez.

**Tecnologías:** Python, pandas, Streamlit y Plotly.

**Demuestra:**

- Preparación y agregación de datos.
- Indicadores de liquidez y flujo.
- Visualización centralizada.
- Filtros por fecha y banco.

[Consultar el caso de estudio](projects/dashboard-posicion-flujo/README.md)

## Habilidades

- **Python:** pandas, NumPy, openpyxl, xlrd, Matplotlib, Seaborn y Jupyter Notebook.
- **SQL:** SELECT, WHERE, GROUP BY, HAVING, ORDER BY, agregaciones y JOINs.
- **Power BI:** Power Query, modelado de datos, DAX intermedio, inteligencia de tiempo y dashboards.
- **Excel:** tablas dinámicas, fórmulas avanzadas, Power Query, macros y VBA.
- **Finanzas:** posición y flujo bancario, liquidez, cartera, pasivos, fondeo, conciliación y análisis financiero.
- **ERP:** Odoo en módulos de Contabilidad, Finanzas, CRM, Ventas y Compras.

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/generar_datos_sinteticos.py
python scripts/ejecutar_pipeline.py
streamlit run dashboard/app.py
```

## Privacidad

Antes de publicar una actualización, revisar [PRIVACY_CHECKLIST.md](PRIVACY_CHECKLIST.md). Los nombres, montos y entidades del demo son ficticios y no deben sustituirse por información laboral real.

## Alcance público

El objetivo de este repositorio es demostrar arquitectura, transformación de datos, validaciones y visualización. Las reglas financieras son representativas y no reproducen contratos, formatos ni metodologías internas de terceros.
