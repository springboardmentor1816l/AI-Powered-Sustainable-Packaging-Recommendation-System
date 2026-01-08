"""
Test Runner Script for EcoPackAI E2E Tests
Run this script to execute the complete test suite
"""

import subprocess
import sys
import os
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import playwright
        import pytest
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\n📦 Installing dependencies...")
        
        # Install dependencies
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", 
            "requirements-e2e.txt"
        ], check=True)
        
        # Install Playwright browsers
        subprocess.run([
            sys.executable, "-m", "playwright", "install", "chromium"
        ], check=True)
        
        print("✅ Dependencies installed successfully")
        return True


def check_servers():
    """Check if frontend and backend servers are running"""
    print("\n🔍 Checking if servers are running...")
    
    import socket
    
    def is_port_open(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    
    frontend_running = is_port_open("localhost", 8080)
    backend_running = is_port_open("localhost", 5000)
    
    if not frontend_running:
        print("⚠️  Frontend server not detected on port 8080")
        print("   Please start the frontend server before running tests")
        print("   Tip: Use 'python -m http.server 8080' in the frontend directory")
        return False
    
    if not backend_running:
        print("⚠️  Backend server not detected on port 5000")
        print("   Please start the backend server before running tests")
        print("   Tip: Run 'python backend/app.py'")
        return False
    
    print("✅ Both frontend and backend servers are running")
    return True


def run_tests(test_type="all"):
    """Run the test suite"""
    print(f"\n🚀 Running {test_type} tests...\n")
    
    # Create reports directory
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Prepare pytest arguments
    pytest_args = [
        "test_e2e_ui.py",
        "-v",
        "--html=reports/e2e_test_report.html",
        "--self-contained-html",
    ]
    
    # Add markers based on test type
    if test_type == "smoke":
        pytest_args.append("-m smoke")
    elif test_type == "regression":
        pytest_args.append("-m regression")
    elif test_type == "ui":
        pytest_args.append("-m ui")
    
    # Run tests
    result = subprocess.run(
        [sys.executable, "-m", "pytest"] + pytest_args,
        cwd=Path(__file__).parent
    )
    
    # Print results
    print("\n" + "="*60)
    if result.returncode == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. Check the report for details.")
    print("="*60)
    
    print(f"\n📊 Test report generated: {reports_dir / 'e2e_test_report.html'}")
    
    return result.returncode


def main():
    """Main execution function"""
    print("="*60)
    print("🧪 EcoPackAI E2E Test Suite")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed")
        return 1
    
    # Check servers
    if not check_servers():
        print("\n❌ Server check failed")
        print("\nPlease start the required servers and try again:")
        print("  1. Frontend: cd frontend && python -m http.server 8080")
        print("  2. Backend: python backend/app.py")
        return 1
    
    # Run tests
    test_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    exit_code = run_tests(test_type)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
