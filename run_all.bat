@echo off
title TaskFlow - Launch All Services
echo ==================================================
echo Menjalankan TaskFlow (Backend FastAPI + Frontend Vue 3)...
echo ==================================================

start "TaskFlow Backend API" cmd /c "%~dp0run_backend.bat"
timeout /t 3 /nobreak >nul
start "TaskFlow Frontend UI" cmd /c "%~dp0run_frontend.bat"

echo.
echo Service berhasil dijalankan di jendela terpisah!
echo Backend API : http://localhost:8000
echo Swagger Docs: http://localhost:8000/docs
echo Frontend App: http://localhost:5173
echo.

