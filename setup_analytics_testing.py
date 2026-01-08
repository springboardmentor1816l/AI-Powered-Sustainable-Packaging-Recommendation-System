"""
Quick Setup Script for EcoPackAI Analytics & Testing
Run this script to set up and verify the complete implementation
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_step(number, text):
    """Print a step with number"""
    print(f"\n[{number}/7] {text}")


def check_python_version():
    """Verify Python version"""
    print_step(1, "Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ Python 3.8 or higher required")
        return False
    
    print("   ✅ Python version compatible")
    return True


def install_backend_dependencies():
    """Install backend requirements"""
    print_step(2, "Installing backend dependencies...")
    
    requirements_file = Path(__file__).parent / "environments" / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"   ⚠️  Requirements file not found: {requirements_file}")
        return False
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True,
            capture_output=True
        )
        print("   ✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to install dependencies: {e}")
        return False


def install_test_dependencies():
    """Install testing requirements"""
    print_step(3, "Installing E2E testing dependencies...")
    
    requirements_file = Path(__file__).parent / "tests" / "requirements-e2e.txt"
    
    if not requirements_file.exists():
        print(f"   ⚠️  Test requirements file not found: {requirements_file}")
        return False
    
    try:
        # Install Python packages
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True,
            capture_output=True
        )
        
        # Install Playwright browsers
        print("   Installing Playwright browsers...")
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
            capture_output=True
        )
        
        print("   ✅ Test dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to install test dependencies: {e}")
        return False


def verify_file_structure():
    """Verify all required files exist"""
    print_step(4, "Verifying file structure...")
    
    required_files = [
        "frontend/analytics.html",
        "frontend/js/analytics.js",
        "frontend/css/styles.css",
        "tests/test_e2e_ui.py",
        "tests/run_e2e_tests.py",
        "tests/conftest.py",
        "docs/analytics_dashboard_guide.md",
        "docs/e2e_testing_guide.md",
        "docs/QUICKSTART_ANALYTICS_TESTING.md"
    ]
    
    base_path = Path(__file__).parent
    all_exist = True
    
    for file in required_files:
        file_path = base_path / file
        if file_path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            all_exist = False
    
    if all_exist:
        print("   ✅ All required files present")
    else:
        print("   ⚠️  Some files are missing")
    
    return all_exist


def create_reports_directory():
    """Create test reports directory"""
    print_step(5, "Creating reports directory...")
    
    reports_dir = Path(__file__).parent / "tests" / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    print(f"   ✅ Reports directory ready: {reports_dir}")
    return True


def display_server_instructions():
    """Display instructions for starting servers"""
    print_step(6, "Server startup instructions...")
    
    print("\n   To start the application, open 2 terminals:")
    print("\n   Terminal 1 - Backend Server:")
    print("   ---------------------------")
    print("   cd backend")
    print("   python app.py")
    print("\n   Terminal 2 - Frontend Server:")
    print("   -----------------------------")
    print("   cd frontend")
    print("   python -m http.server 8080")
    
    print("\n   ⚠️  Keep both terminals running during testing")
    return True


def display_testing_instructions():
    """Display instructions for running tests"""
    print_step(7, "Testing instructions...")
    
    print("\n   To run E2E tests (after starting servers):")
    print("   ------------------------------------------")
    print("   cd tests")
    print("   python run_e2e_tests.py")
    
    print("\n   To view test report:")
    print("   -------------------")
    print("   start tests/reports/e2e_test_report.html")
    
    print("\n   To use analytics dashboard:")
    print("   --------------------------")
    print("   1. Open: http://localhost:8080")
    print("   2. Click 'Product Input'")
    print("   3. Fill form and submit")
    print("   4. Click 'Analytics' to view charts")
    print("   5. Use export buttons for CSV/PDF")
    
    return True


def create_quick_reference():
    """Create a quick reference file"""
    quick_ref = """
# EcoPackAI - Quick Reference Commands

## Start Application
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend  
cd frontend
python -m http.server 8080
```

## Run Tests
```bash
# Terminal 3: E2E Tests
cd tests
python run_e2e_tests.py
```

## URLs
- Frontend: http://localhost:8080
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/health
- Analytics: http://localhost:8080/analytics.html

## Test Report
- Location: tests/reports/e2e_test_report.html
- Open: `start tests/reports/e2e_test_report.html`

## Export Files
- Downloads to: Your browser's Downloads folder
- Format: EcoPackAI_Report_[timestamp].csv/pdf

## Documentation
- Quick Start: docs/QUICKSTART_ANALYTICS_TESTING.md
- Analytics Guide: docs/analytics_dashboard_guide.md  
- Testing Guide: docs/e2e_testing_guide.md
- Summary: ANALYTICS_TESTING_SUMMARY.md

## Test Commands
```bash
# All tests
pytest test_e2e_ui.py -v

# Specific test
pytest test_e2e_ui.py::TestEcoPackAIWorkflow::test_complete_prediction_workflow -v

# Export tests only
pytest test_e2e_ui.py -k "export" -v
```

## Troubleshooting
1. Check servers are running: `netstat -an | findstr "8080 5000"`
2. View browser console for errors
3. Clear browser cache and localStorage
4. Verify dependencies: `pip list | findstr "playwright pytest"`
"""
    
    quick_ref_file = Path(__file__).parent / "QUICK_REFERENCE.md"
    with open(quick_ref_file, "w") as f:
        f.write(quick_ref)
    
    print(f"\n   ✅ Quick reference created: {quick_ref_file}")


def main():
    """Main setup function"""
    print_header("EcoPackAI Analytics & Testing Setup")
    
    # Run setup steps
    steps = [
        check_python_version,
        install_backend_dependencies,
        install_test_dependencies,
        verify_file_structure,
        create_reports_directory,
        display_server_instructions,
        display_testing_instructions
    ]
    
    success = True
    for step in steps:
        if not step():
            success = False
            break
    
    # Create quick reference
    create_quick_reference()
    
    # Print final status
    print_header("Setup Complete!" if success else "Setup Failed")
    
    if success:
        print("\n✅ All setup steps completed successfully!")
        print("\n📚 Next steps:")
        print("   1. Review: QUICK_REFERENCE.md")
        print("   2. Start servers (see instructions above)")
        print("   3. Run tests: cd tests && python run_e2e_tests.py")
        print("   4. View analytics: http://localhost:8080/analytics.html")
        print("\n📖 Documentation:")
        print("   - Quick Start: docs/QUICKSTART_ANALYTICS_TESTING.md")
        print("   - Full Summary: ANALYTICS_TESTING_SUMMARY.md")
    else:
        print("\n❌ Setup encountered errors")
        print("   Please review the output above and fix any issues")
    
    print("\n" + "="*60 + "\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
