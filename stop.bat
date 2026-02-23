@echo off
echo =========================================
echo   YYS Guess System - Stop Services
echo =========================================
echo.

echo [Info] Stopping services...
echo.

:: Kill Python processes (backend)
echo [1/2] Stopping backend service (Python)...
taskkill /F /IM python.exe 2>nul
if errorlevel 1 (
    echo       No Python process found
echo.
) else (
    echo       Backend service stopped
echo.
)

:: Kill Node.js processes (frontend)
echo [2/2] Stopping frontend service (Node.js)...
taskkill /F /IM node.exe 2>nul
if errorlevel 1 (
    echo       No Node.js process found
echo.
) else (
    echo       Frontend service stopped
echo.
)

echo =========================================
echo   All services stopped!
echo =========================================
echo.
pause
