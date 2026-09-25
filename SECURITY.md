# Seguridad y privacidad

Este repositorio acepta únicamente código demostrativo y datos sintéticos.

## No publicar

- Archivos obtenidos de un empleador o cliente.
- Nombres reales de personas, clientes, bancos, fondeadores o proveedores.
- Cuentas, CLABE, contratos, saldos, tasas, vencimientos o cifras regulatorias reales.
- Correos internos, rutas de red, credenciales, tokens, archivos `.env` o capturas laborales.
- Lógica propietaria, plantillas o formatos internos de terceros.

## Antes de cada publicación

1. Ejecutar `python -m pytest -q`.
2. Revisar `git diff --staged` archivo por archivo.
3. Ejecutar las búsquedas descritas en `PRIVACY_CHECKLIST.md`.
4. Revisar visualmente todas las imágenes nuevas.
5. Confirmar que los resultados procedan del generador sintético incluido.

Si un dato genera duda, no debe publicarse.
