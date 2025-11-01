@echo off
echo ========================================
echo Image to Desmos - Setup Script
echo ========================================
echo.

echo [1/3] Installing Python dependencies...
cd backend
pip install -r requirements.txt
cd ..
echo.

echo [2/3] Installing Node.js dependencies...
cd frontend
call npm install
cd ..
echo.

echo [3/3] Creating necessary directories...
if not exist "backend\uploads" mkdir backend\uploads
if not exist "backend\output" mkdir backend\output
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo 1. Run start-backend.bat in one terminal
echo 2. Run start-frontend.bat in another terminal
echo 3. Open http://localhost:5173 in your browser
echo.
pause
