@echo off
REM Claude Context Manager - Progress Report Generator
REM Generates comprehensive progress reports for all tracked projects

echo.
echo ========================================
echo  Claude Context Manager
echo  Progress Report Generator  
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Run the Python script
echo 🔄 Generating comprehensive progress reports...
echo.

python generate-progress-reports.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ Progress reports generated successfully!
    echo 📁 Check the reports/ folder for output files
    echo.
    echo Available reports:
    echo   - progress_report.json    ^(Machine-readable data^)
    echo   - progress_report.md      ^(Human-readable summary^)  
    echo   - progress_report.html    ^(Interactive dashboard^)
    echo.
    
    REM Ask if user wants to open HTML report
    set /p "openhtml=Would you like to open the HTML report? (y/n): "
    if /i "%openhtml%"=="y" (
        echo Opening HTML report...
        start "..\reports\progress_report.html"
    )
    
) else (
    echo.
    echo ❌ Report generation failed!
    echo Please check the error messages above.
)

echo.
pause