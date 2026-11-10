@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Preparing Windows EXE installer...
where py >nul 2>&1 || (echo Python 3 launcher is required & pause & exit /b 1)
py -3 -m pip install pyinstaller
if errorlevel 1 (echo Could not install PyInstaller & pause & exit /b 1)
if not exist node_modules call npm install
call npm run build:web
if errorlevel 1 (echo Frontend build failed & pause & exit /b 1)
py -3 -m PyInstaller --onefile --clean --noconfirm --name ues-backend --distpath dist-backend --workpath build-backend --specpath build-backend backend/src/http_server.py
if errorlevel 1 (echo Backend build failed & pause & exit /b 1)
call npx electron-builder --win nsis
if errorlevel 1 (echo EXE build failed & pause & exit /b 1)
echo Finished. Open the release folder.
pause
