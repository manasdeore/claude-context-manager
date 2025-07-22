@echo off
REM Claude Context Manager - Project Viewer (Windows)
echo Loading Claude Context Manager...

REM Try different Python commands
python scripts\view-projects.py 2>nul && goto :end
python3 scripts\view-projects.py 2>nul && goto :end
py scripts\view-projects.py 2>nul && goto :end

echo Python not found! Please install Python or use the manual method below:
echo.
echo === MANUAL PROJECT VIEW ===
type projects.json
echo.
echo Run this batch file to see your projects anytime.

:end