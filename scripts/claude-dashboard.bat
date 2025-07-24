@echo off
title Claude Context Manager Dashboard

REM Change to the script directory
cd /d "%~dp0"

echo Starting Claude Dashboard...

REM Try different Python commands
python claude-dashboard.py 2>nul && goto :end
python3 claude-dashboard.py 2>nul && goto :end
py claude-dashboard.py 2>nul && goto :end

REM If Python is not found, show error and fallback
echo.
echo ================================
echo   Python not found!
echo ================================
echo.
echo Please install Python 3.7+ to use the interactive dashboard.
echo.
echo Falling back to basic project viewer...
echo.
pause
echo.

REM Run the basic viewer instead
call view-projects.bat

:end
echo.
echo Dashboard closed. Press any key to exit...
pause >nul