@echo off
title TaskFlow - Frontend UI (Vue 3 + Vite)
echo ==================================================
echo Starting TaskFlow Frontend Client...
echo URL: http://localhost:5173
echo ==================================================
cd /d "%~dp0frontend"
npm run dev
pause

