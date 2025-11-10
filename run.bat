@echo off
chcp 65001 > nul
echo ========================================
echo   Business Card Manager - Starting...
echo ========================================
echo.

REM Change to project directory
cd /d %~dp0

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found. Using system Python.
    echo To create virtual environment, run: python -m venv venv
    echo.
)

REM Start Streamlit app
echo Starting Streamlit app...
echo Browser will open automatically. If not, go to:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo.

streamlit run app.py

pause
