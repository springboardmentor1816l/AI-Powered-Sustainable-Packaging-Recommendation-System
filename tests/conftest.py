"""
Pytest configuration and fixtures for EcoPackAI E2E tests
"""

import pytest
from playwright.sync_api import Browser, BrowserContext, Page
import os
from pathlib import Path


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context with additional settings"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
        "permissions": ["downloads"],
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments"""
    return {
        **browser_type_launch_args,
        "headless": False,  # Set to True for CI/CD
        "slow_mo": 100,     # Slow down operations for visibility
    }


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create a new browser context for each test"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page for each test"""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def test_output_dir():
    """Create and return test output directory"""
    output_dir = Path(__file__).parent / "test_outputs"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@pytest.fixture(scope="session")
def screenshots_dir(test_output_dir):
    """Create and return screenshots directory"""
    screenshots_dir = test_output_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    return screenshots_dir


@pytest.fixture(scope="session")
def downloads_dir(test_output_dir):
    """Create and return downloads directory"""
    downloads_dir = test_output_dir / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    return downloads_dir


def pytest_configure(config):
    """Pytest hook for configuration"""
    # Create reports directory
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Add custom markers
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression suite")
    config.addinivalue_line("markers", "ui: User interface tests")
    config.addinivalue_line("markers", "performance: Performance tests")


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "EcoPackAI E2E Test Report"
