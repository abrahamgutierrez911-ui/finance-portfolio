# Lista de seguridad antes de publicar

## Nunca publicar

- Nombres reales de clientes, fondeadores, proveedores o empleados.
- Números de cuenta, CLABE, tarjetas, contratos, créditos o referencias bancarias.
- Saldos, tasas, vencimientos, líneas autorizadas o cifras regulatorias reales.
- Archivos de Excel, PDF, Word, correos o capturas obtenidos en el trabajo.
- Código propiedad de un empleador o lógica que revele procesos internos confidenciales.
- Contraseñas, tokens, archivos `.env`, rutas de red, usuarios o credenciales.
- Logotipos o documentos corporativos sin autorización.

## Revisión obligatoria

1. Confirmar que todos los datos sean sintéticos.
2. Buscar nombres de empresas, personas y fondeadores reales.
3. Buscar patrones de cuentas, CLABE y correos internos.
4. Revisar el historial de Git, no solo los archivos actuales.
5. Abrir cada captura y comprobar que no contenga nombres, montos o rutas reales.
6. Ejecutar `git status` y revisar individualmente cada archivo antes del commit.
7. Si un dato genera duda, no publicarlo.

## Comandos de revisión sugeridos

```bash
git status
git diff --staged
rg -n -i "clabe|cuenta|contrato|cliente|password|token|secret|apikey|correo" .
```

La búsqueda automática no reemplaza la revisión manual.

