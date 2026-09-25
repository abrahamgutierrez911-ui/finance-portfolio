@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    py -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
endlocal
