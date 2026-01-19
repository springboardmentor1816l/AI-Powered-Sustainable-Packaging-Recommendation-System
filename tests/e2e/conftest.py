"""
Playwright Configuration for E2E Tests
=======================================

Configuration file for Playwright browser automation tests.

Author: EcoPackAI Team
Date: 2026-01-12
"""

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_context():
    """Create a browser context for testing"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        yield context
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """Create a new page for each test"""
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before running tests"""
    print("\n" + "="*60)
    print("Starting EcoPackAI E2E Test Suite")
    print("="*60)
    yield
    print("\n" + "="*60)
    print("E2E Test Suite Complete")
    print("="*60)
