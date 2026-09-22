# Publicación en GitHub

## 1. Revisión de privacidad

Leer y completar `PRIVACY_CHECKLIST.md`. No copiar archivos del trabajo a este repositorio.

## 2. Crear el repositorio

En GitHub, crear un repositorio público llamado `portfolio-data-finance` sin agregar README, licencia ni `.gitignore`, porque ya están incluidos aquí.

## 3. Publicar desde la terminal

Sustituir `TU_USUARIO` por el usuario real de GitHub:

```bash
git init
git add .
git status
git diff --staged
git commit -m "Portafolio inicial con datos sintéticos"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/portfolio-data-finance.git
git push -u origin main
```

## 4. Configurar el perfil

- Fijar el repositorio en el perfil de GitHub.
- Agregar una descripción breve: `Portafolio de análisis de datos, BI y automatización financiera con Python, SQL y Power BI`.
- Añadir temas: `python`, `pandas`, `power-bi`, `sql`, `finance`, `data-analysis`, `automation`.

## 5. Capturas seguras

Ejecutar los demos con datos sintéticos y guardar únicamente capturas de esos resultados en `assets/`. Revisar manualmente cada imagen antes de publicarla.

