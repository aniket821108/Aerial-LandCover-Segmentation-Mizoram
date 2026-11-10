@echo off
echo =====================================================================
echo  Starting AeroSeg AI Full-Stack Platform (MERN + Python ML)
echo =====================================================================

start "AeroSeg Python ML Service [Port 8000]" cmd /k "cd ml_service && python -m uvicorn service:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

start "AeroSeg Express Backend Gateway [Port 5000]" cmd /k "cd server && npm run dev"

timeout /t 3 /nobreak >nul

start "AeroSeg React Frontend [Port 5173]" cmd /k "cd client && npm run dev"

echo.
echo All 3 services are launching in separate windows!
echo - React Dashboard : http://localhost:5173
echo - Express Backend : http://localhost:5000
echo - Python ML Micro : http://localhost:8000
echo =====================================================================
