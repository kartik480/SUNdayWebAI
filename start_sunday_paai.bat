@echo off
echo 🚀 Starting SUNDAY-PAAI - Both Frontend and Backend...
echo ==================================================

echo 🤖 Starting Flask Backend...
start "Flask Backend" cmd /k "python improved_app.py"

echo ⏳ Waiting for Flask to start...
timeout /t 3 /nobreak > nul

echo ⚛️ Starting Next.js Frontend...
start "Next.js Frontend" cmd /k "npm run dev"

echo ✅ Both servers are starting!
echo 🌐 Frontend: http://localhost:3000
echo 🔗 Backend: http://localhost:8080
echo.
echo Press any key to close this window...
pause > nul 