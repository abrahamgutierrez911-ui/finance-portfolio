# AutomaTES | Automatización de reportes financieros

## Problema profesional

La preparación manual de múltiples reportes financieros requería consolidar archivos con estructuras diferentes, validar cifras y generar entregables separados. El ciclo completo podía tomar entre una y dos semanas.

## Reconstrucción pública

La versión publicada reproduce el tipo de reto sin utilizar archivos, formatos ni reglas confidenciales:

1. Genera estados financieros, pasivos, cartera, vencimientos y movimientos bancarios ficticios.
2. Valida columnas, tipos de datos y disponibilidad de archivos.
3. Limpia y homologa conceptos, fechas, montos y categorías.
4. Construye once entregables principales, incluidos controles y conciliaciones.
5. Genera tres reportes para cada uno de 13 fondeadores ficticios.
6. Registra cada etapa en una bitácora.
7. Permite revisar las tablas y descargar 52 archivos en un ZIP: once entregables, 39 reportes, una bitácora y un manifiesto de integridad.

## Cómo verlo

```bash
streamlit run automates_app.py
```

La interfaz muestra:

- Estados Financieros Base.
- Maestro de Pasivos Base.
- Reporte de Cartera.
- Brecha de Liquidez.
- Validación de trazabilidad.
- Conciliación contra cifras reportadas y tolerancias.
- Matriz de controles de integridad, calidad, cálculo, límites y riesgo.
- Calendario de vencimientos, utilización de líneas y covenants.
- Resumen ejecutivo.
- Bitácora con identificador de ejecución y duración acumulada.
- Manifiesto con tamaño y huella SHA-256 de cada Excel.
- Descarga del paquete completo de resultados.

## Resultado profesional relacionado

La solución original y el dashboard asociado redujeron aproximadamente 75% el tiempo destinado a estas actividades, llevando el procesamiento total de una o dos semanas a dos o tres días.

## Tecnologías

Python, pandas, NumPy, openpyxl, Excel, Streamlit, validación de datos, ETL, pruebas y generación de bitácoras.

## Límites de privacidad

El código fue reescrito para el portafolio. No reproduce interfaces, plantillas, nombres, formatos, cifras, reglas, rutas o lógica interna de ningún empleador.
