@echo off
title TaskFlow - Backend API (FastAPI)
echo ==================================================
echo Starting TaskFlow Backend API Server...
echo URL: http://localhost:8000
echo Swagger Docs: http://localhost:8000/docs
echo ==================================================
cd /d "%~dp0backend"
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment tidak ditemukan.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause

