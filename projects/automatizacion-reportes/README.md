# Automatización de reportes financieros

## Problema

La preparación manual de múltiples reportes financieros requería consolidar archivos con estructuras diferentes, validar cifras y generar entregables separados. El ciclo completo podía tomar entre una y dos semanas.

## Solución pública reconstruida

Este proyecto reproduce el tipo de reto con información totalmente sintética:

1. Genera estados financieros, pasivos, cartera, vencimientos y movimientos bancarios ficticios.
2. Limpia, homologa y valida fechas, montos, columnas y categorías.
3. Construye Estados Financieros Base y Maestro de Pasivos Base.
4. Calcula una Brecha de Liquidez demostrativa por periodos.
5. Consolida el Reporte de Cartera y valida trazabilidad contra sus bases origen.
6. Genera tres reportes para cada uno de 13 fondeadores: resumen, vencimientos y flujo.
7. Exporta 39 archivos Excel y una bitácora de ejecución.

## Resultado profesional relacionado

La solución original y el dashboard asociado redujeron aproximadamente 75% el tiempo dedicado a las actividades, llevando el procesamiento total de una o dos semanas a dos o tres días.

## Tecnologías

- Python
- pandas
- NumPy
- openpyxl
- Excel
- Validación de datos y ETL

## Privacidad

El código fue reescrito específicamente para este portafolio. Los nombres, montos, fechas y reglas son ficticios y no reproducen archivos, plantillas, metodologías ni lógica confidencial de ninguna empresa.
