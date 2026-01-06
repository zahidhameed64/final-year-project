@echo off
setlocal
echo ==========================================
echo Starting Data-to-Narrative Project
echo ==========================================

REM --- 1. Python Detection ---
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found in global PATH. Checking common locations...
    if exist "C:\Users\A C\anaconda3\python.exe" (
        set "PYTHON_EXE=C:\Users\A C\anaconda3\python.exe"
        echo Found Anaconda Python.
    ) else (
        echo Error: Python not found. Please ensure Python is installed.
        pause
        exit /b 1
    )
) else (
    set "PYTHON_EXE=python"
)

REM --- 2. Install/Check Backend Dependencies ---
if exist "backend\requirements.txt" (
    echo Installing/Updating Backend Dependencies...
    "%PYTHON_EXE%" -m pip install -r backend\requirements.txt
)

REM --- 3. Start Backend ---
echo Starting Flask Backend (Port 5000)...
start "Flask Backend" "%PYTHON_EXE%" backend\app.py

REM --- 4. Start Frontend ---
cd frontend
if not exist node_modules (
    echo Node modules not found. Installing...
    call npm install
)

echo Starting Next.js Frontend (Port 3000)...
start "Next.js Frontend" npm run dev

REM --- 5. Open Browser ---
echo Launching browser in 5 seconds...
timeout /t 5 >nul
start http://localhost:3000

echo.
echo Application started!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:5000
echo.
pause
