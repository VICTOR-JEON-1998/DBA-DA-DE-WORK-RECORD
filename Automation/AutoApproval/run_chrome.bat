@echo off
cd /d "%~dp0"

echo Starting Chrome for DBSAfer Automation...
echo Please log in to DBSAfer in the opened window.
echo Do NOT close this window. Run the Python script after logging in.

cd /d "C:\Program Files\Google\Chrome\Application"
if not exist chrome.exe (
    cd /d "C:\Program Files (x86)\Google\Chrome\Application"
)

:: Use relative path for profile so it works on other computers
start chrome.exe --remote-debugging-port=9222 --user-data-dir="%~dp0chrome_debug_profile" "https://dbsafer.mistobrand.com/works/"
echo Chrome launched on port 9222.

echo.
echo Launching Python Automation Bot in 3 seconds...
timeout /t 3

:: Check if local venv exists (for the developer)
if exist "%~dp0.venv\Scripts\python.exe" (
    start "DBSafer Automation Bot" "%~dp0.venv\Scripts\python.exe" "%~dp0main.py"
) else (
    :: Fallback to global python (for other users)
    start "DBSafer Automation Bot" python "%~dp0main.py"
)

echo.
echo =======================================================
echo  Please log in to DBSAfer in the Chrome window.
echo  The bot is running in the OTHER window and will wait.
echo =======================================================
pause
