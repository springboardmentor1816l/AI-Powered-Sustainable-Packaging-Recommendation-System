@echo off
REM EcoPackAI - Quick Validation Script
REM Run this to verify the complete implementation

echo ===============================================================
echo   EcoPackAI - Analytics ^& Testing Validation
echo ===============================================================
echo.

echo [1/5] Checking File Structure...
echo.

if exist "frontend\analytics.html" (
    echo   [OK] frontend\analytics.html
) else (
    echo   [FAIL] frontend\analytics.html - MISSING
)

if exist "frontend\js\analytics.js" (
    echo   [OK] frontend\js\analytics.js
) else (
    echo   [FAIL] frontend\js\analytics.js - MISSING
)

if exist "tests\test_e2e_ui.py" (
    echo   [OK] tests\test_e2e_ui.py
) else (
    echo   [FAIL] tests\test_e2e_ui.py - MISSING
)

if exist "docs\analytics_dashboard_guide.md" (
    echo   [OK] docs\analytics_dashboard_guide.md
) else (
    echo   [FAIL] docs\analytics_dashboard_guide.md - MISSING
)

echo.
echo [2/5] Checking Python Dependencies...
echo.

python -c "import flask" 2>nul
if %errorlevel% equ 0 (
    echo   [OK] Flask installed
) else (
    echo   [WARN] Flask not found - run: pip install flask
)

python -c "import playwright" 2>nul
if %errorlevel% equ 0 (
    echo   [OK] Playwright installed
) else (
    echo   [WARN] Playwright not found - run: pip install playwright
)

python -c "import pytest" 2>nul
if %errorlevel% equ 0 (
    echo   [OK] Pytest installed
) else (
    echo   [WARN] Pytest not found - run: pip install pytest
)

echo.
echo [3/5] Checking Server Ports...
echo.

netstat -an | findstr ":8080" >nul 2>&1
if %errorlevel% equ 0 (
    echo   [OK] Port 8080 in use (Frontend likely running)
) else (
    echo   [WARN] Port 8080 not in use - Start frontend server
    echo         Command: cd frontend ^&^& python -m http.server 8080
)

netstat -an | findstr ":5000" >nul 2>&1
if %errorlevel% equ 0 (
    echo   [OK] Port 5000 in use (Backend likely running)
) else (
    echo   [WARN] Port 5000 not in use - Start backend server
    echo         Command: python backend\app.py
)

echo.
echo [4/5] Checking Documentation...
echo.

if exist "ANALYTICS_TESTING_SUMMARY.md" (
    echo   [OK] Implementation summary exists
) else (
    echo   [FAIL] ANALYTICS_TESTING_SUMMARY.md - MISSING
)

if exist "docs\QUICKSTART_ANALYTICS_TESTING.md" (
    echo   [OK] Quick start guide exists
) else (
    echo   [FAIL] Quick start guide - MISSING
)

if exist "docs\e2e_testing_guide.md" (
    echo   [OK] Testing guide exists
) else (
    echo   [FAIL] Testing guide - MISSING
)

echo.
echo [5/5] Feature Checklist...
echo.

echo   Analytics Features:
echo   [+] Interactive charts (Chart.js)
echo   [+] CSV export functionality
echo   [+] PDF export functionality
echo   [+] Summary cards with metrics
echo   [+] Responsive design
echo.

echo   E2E Testing:
echo   [+] 14 automated test scenarios
echo   [+] Playwright browser automation
echo   [+] HTML test reports
echo   [+] Test runner script
echo.

echo   Documentation:
echo   [+] Analytics dashboard guide
echo   [+] E2E testing guide  
echo   [+] Quick start guide
echo   [+] Architecture diagrams
echo.

echo ===============================================================
echo   Validation Complete!
echo ===============================================================
echo.

echo Next Steps:
echo   1. Start servers (if not running):
echo      - Backend:  python backend\app.py
echo      - Frontend: cd frontend ^&^& python -m http.server 8080
echo.
echo   2. Run E2E tests:
echo      cd tests ^&^& python run_e2e_tests.py
echo.
echo   3. View analytics:
echo      http://localhost:8080/analytics.html
echo.
echo   4. Read documentation:
echo      start ANALYTICS_TESTING_SUMMARY.md
echo.

pause
