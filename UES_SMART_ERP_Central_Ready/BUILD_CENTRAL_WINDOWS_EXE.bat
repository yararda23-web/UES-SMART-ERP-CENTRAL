@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Building UES Smart ERP CENTRAL desktop client...
where node >nul 2>&1 || (echo Node.js is required & pause & exit /b 1)
if not exist node_modules call npm.cmd install
if errorlevel 1 (echo NPM installation failed & pause & exit /b 1)
call npx.cmd electron-builder --win nsis
if errorlevel 1 (echo Build failed. Review output above & pause & exit /b 1)
echo Finished: release\UES-Smart-ERP-Central-Setup-3.0.0.exe
pause
