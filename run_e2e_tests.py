"""
E2E Test Runner Script
======================

Convenience script to run end-to-end UI tests with different configurations.

Usage:
    python run_e2e_tests.py                 # Run all tests
    python run_e2e_tests.py --headed        # Run with visible browser
    python run_e2e_tests.py --specific test_name  # Run specific test

Author: EcoPackAI Team
Date: 2026-01-12
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_tests(headed=False, specific_test=None, verbose=False):
    """
    Run E2E tests with specified configuration
    
    Args:
        headed: Run with visible browser
        specific_test: Run only specific test
        verbose: Verbose output
    """
    # Base command
    cmd = ["pytest", "tests/e2e/"]
    
    # Add verbose flag
    if verbose:
        cmd.extend(["-v", "-s"])
    else:
        cmd.append("-v")
    
    # Run specific test
    if specific_test:
        cmd[1] = f"tests/e2e/test_ui_workflow.py::{specific_test}"
    
    # Add pytest-playwright flags
    if headed:
        cmd.append("--headed")
    
    # Add color output
    cmd.append("--color=yes")
    
    print("="*60)
    print("EcoPackAI E2E Test Runner")
    print("="*60)
    print(f"Command: {' '.join(cmd)}")
    print("="*60)
    print()
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        return result.returncode
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        return 130
    except Exception as e:
        print(f"\nError running tests: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Run EcoPackAI E2E tests")
    
    parser.add_argument(
        '--headed',
        action='store_true',
        help='Run tests with visible browser'
    )
    
    parser.add_argument(
        '--specific',
        type=str,
        help='Run specific test (e.g., test_home_page_loads)',
        metavar='TEST_NAME'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '--install-browsers',
        action='store_true',
        help='Install Playwright browsers'
    )
    
    args = parser.parse_args()
    
    # Install browsers if requested
    if args.install_browsers:
        print("Installing Playwright browsers...")
        subprocess.run(["playwright", "install", "chromium"])
        print("\nBrowsers installed successfully!")
        return 0
    
    # Run tests
    return run_tests(
        headed=args.headed,
        specific_test=args.specific,
        verbose=args.verbose
    )


if __name__ == "__main__":
    sys.exit(main())
