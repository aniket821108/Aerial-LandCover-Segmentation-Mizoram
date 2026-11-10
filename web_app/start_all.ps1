# AeroSeg AI - One-Click Launcher for PowerShell
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " Starting AeroSeg AI Full-Stack Platform (MERN + Python Microservice)" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

# 1. Start Python ML Microservice
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PSScriptRoot\ml_service'; python -m uvicorn service:app --host 127.0.0.1 --port 8000 --reload"

Start-Sleep -Seconds 3

# 2. Start Express Backend Gateway
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PSScriptRoot\server'; npm run dev"

Start-Sleep -Seconds 3

# 3. Start Vite React Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PSScriptRoot\client'; npm run dev"

Write-Host "`nAll 3 services successfully launched!" -ForegroundColor Green
Write-Host "  -> React UI Dashboard : http://localhost:5173" -ForegroundColor Yellow
Write-Host "  -> Express API Gateway: http://localhost:5000" -ForegroundColor Yellow
Write-Host "  -> Python ML Service  : http://localhost:8000" -ForegroundColor Yellow
