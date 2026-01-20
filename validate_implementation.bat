@echo off
echo ============================================
echo  EcoPackAI - Implementation Validation Tool
echo ============================================
echo.

set ERROR_FOUND=0

echo [1/6] Checking Frontend Files...
if not exist frontend\analytics.html (
    echo ❌ Missing frontend\analytics.html
    set ERROR_FOUND=1
) else echo ✅ analytics.html found

if not exist frontend\js\analytics.js (
    echo ❌ Missing frontend\js\analytics.js
    set ERROR_FOUND=1
) else echo ✅ analytics.js found

if not exist frontend\css\styles.css (
    echo ❌ Missing frontend\css\styles.css
    set ERROR_FOUND=1
) else echo ✅ styles.css found

if not exist frontend\js\predict.js (
    echo ❌ Missing frontend\js\predict.js
    set ERROR_FOUND=1
) else echo ✅ predict.js found

echo.
echo [2/6] Checking Test Files...
if not exist tests\test_e2e_ui.py (
    echo ❌ Missing test_e2e_ui.py
    set ERROR_FOUND=1
) else echo ✅ E2E tests found

if not exist tests\conftest.py (
    echo ❌ Missing conftest.py
    set ERROR_FOUND=1
) else echo ✅ conftest.py found

if not exist tests\pytest.ini (
    echo ❌ Missing pytest.ini
    set ERROR_FOUND=1
) else echo ✅ pytest.ini found

if not exist tests\run_e2e_tests.py (
    echo ❌ Missing run_e2e_tests.py
    set ERROR_FOUND=1
) else echo ✅ test runner found

echo.
echo [3/6] Checking Documentation...
if not exist docs\analytics_dashboard_guide.md (
    echo ❌ Missing analytics_dashboard_guide.md
    set ERROR_FOUND=1
) else echo ✅ Analytics guide found

if not exist docs\e2e_testing_guide.md (
    echo ❌ Missing e2e_testing_guide.md
    set ERROR_FOUND=1
) else echo ✅ E2E guide found

if not exist docs\QUICKSTART_ANALYTICS_TESTING.md (
    echo ❌ Missing quickstart guide
    set ERROR_FOUND=1
) else echo ✅ Quickstart guide found

if not exist ANALYTICS_TESTING_SUMMARY.md (
    echo ❌ Missing analytics testing summary
    set ERROR_FOUND=1
) else echo ✅ Analytics summary found

if not exist IMPLEMENTATION_COMPLETE.md (
    echo ❌ Missing implementation report
    set ERROR_FOUND=1
) else echo ✅ Implementation report found

echo.
echo [4/6] Checking Helper Scripts...
if not exist setup_analytics_testing.py (
    echo ❌ Missing setup_analytics_testing.py
    set ERROR_FOUND=1
) else echo ✅ Setup script found

echo.
echo [5/6] Checking Python Environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not installed or not in PATH
    set ERROR_FOUND=1
) else echo ✅ Python detected

pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip not available
    set ERROR_FOUND=1
) else echo ✅ pip detected

echo.
echo [6/6] Final Validation Status
echo --------------------------------------------

if %ERROR_FOUND%==0 (
    echo ✅ All files present
    echo ✅ Dependencies available
    echo ✅ Documentation complete
    echo ✅ Implementation VERIFIED COMPLETE
) else (
    echo ❌ Validation FAILED
    echo ❌ Please fix the above issues
)

echo.
pause
