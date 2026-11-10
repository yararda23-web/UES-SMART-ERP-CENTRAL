@echo off
chcp 65001 >nul
cd /d "%~dp0"
where node >nul 2>&1 || (echo Node.js is missing. Install Node.js LTS. & pause & exit /b 1)
where py >nul 2>&1 || (where python >nul 2>&1 || (echo Python 3 is missing. Install Python 3. & pause & exit /b 1))
if not exist node_modules call npm install
if not exist frontend\dist\assets\ues.css call npm run build:web
call npm start
if errorlevel 1 pause
