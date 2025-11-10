@echo off
chcp 65001 > nul
echo ========================================
echo   Business Card Manager - Setup
echo ========================================
echo.

REM Change to project directory
cd /d %~dp0

REM Check Python version
echo [1/4] Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed.
    echo Please download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created successfully.
)
echo.

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [4/4] Installing dependencies...
echo This may take a few minutes...
echo.
pip install -r requirements.txt

echo.
echo ========================================
echo   Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Get Gemini API key
echo    https://makersuite.google.com/app/apikey
echo.
echo 2. Get Google Cloud credentials
echo    https://console.cloud.google.com/
echo    - Enable Cloud Vision API
echo    - Enable Google Sheets API
echo    - Create service account and download JSON credentials
echo.
echo 3. Run the app
echo    Double-click run.bat or execute:
echo    streamlit run app.py
echo.
echo For detailed instructions, see SETUP_GUIDE.md
echo.

pause
