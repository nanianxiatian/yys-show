@echo off
chcp 65001 >nul
echo =========================================
echo   YYS Guess Analysis System - Debug Mode
echo =========================================
echo.

:: Check Python environment
echo [Check] Python environment...
python --version
if errorlevel 1 (
    echo [Error] Python not found. Please install Python and add to PATH.
    pause
    exit /b 1
)
echo [Pass] Python is installed
echo.

:: Check Node.js environment
echo [Check] Node.js environment...
node --version
if errorlevel 1 (
    echo [Error] Node.js not found. Please install Node.js and add to PATH.
    pause
    exit /b 1
)
echo [Pass] Node.js is installed
echo.

:: Enter backend directory
cd backend

:: Check virtual environment
echo [Check] Python virtual environment...
if not exist venv (
    echo [Info] Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo [Info] Activating virtual environment...
call venv\Scripts\activate

:: Install backend dependencies
echo [Install] Backend dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [Error] Failed to install backend dependencies.
    pause
    exit /b 1
)
echo [Pass] Backend dependencies installed
echo.

:: Check .env file
echo [Check] Environment variables file...
if not exist .env (
    echo [Warning] .env file not found, creating from example...
    if exist .env.example (
        copy .env.example .env
        echo [Info] Created .env file. Please edit it with your real configuration.
        echo [Info] Especially MYSQL_PASSWORD and SECRET_KEY.
        notepad .env
    ) else (
        echo [Error] .env.example file not found.
        pause
        exit /b 1
    )
) else (
    echo [Pass] .env file exists
)
echo.

:: Initialize database
echo [Init] Database...
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()" 2>nul
echo [Pass] Database initialized
echo.

cd ..

:: Install frontend dependencies
cd frontend
echo [Check] Frontend dependencies...
if not exist node_modules (
    echo [Install] Installing frontend dependencies, please wait...
    npm install
    if errorlevel 1 (
        echo [Error] Failed to install frontend dependencies.
        pause
        exit /b 1
    )
) else (
    echo [Pass] Frontend dependencies installed
)
echo.

cd ..

:: Start services
echo =========================================
echo   All checks passed. Starting services...
echo =========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.

:: Start backend (in new window)
start "Backend Service" cmd /k "cd backend && call venv\Scripts\activate && python run.py"

:: Wait for backend to start
timeout /t 5 /nobreak >nul

:: Start frontend (in new window)
start "Frontend Service" cmd /k "cd frontend && npm run dev"

echo.
echo [Success] Services started!
echo.
echo Instructions:
echo - Backend window: Shows API service logs
echo - Frontend window: Shows frontend dev server logs
echo - Browser will open automatically in 8 seconds
echo.

:: Wait for services to fully start
timeout /t 8 /nobreak >nul

:: Open browser
echo [Info] Opening browser...
start http://localhost:5173

echo [Info] Browser opened. Enjoy!
echo.
pause
