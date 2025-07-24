@echo off
title Project Progress Updater

echo.
echo =====================================
echo   Project Progress Updater
echo =====================================
echo.
echo Triggering project tracker update...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Run the Python updater
python update-progress.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ Update completed successfully!
    echo Dashboard will reflect changes shortly.
) else (
    echo.
    echo ❌ Update failed. Please check the logs.
)

echo.
echo Press any key to close...
pause >nul