# EcoPackAI - End-to-End Testing Documentation

## Overview

This document describes the end-to-end (E2E) testing framework for the EcoPackAI application, including setup, test scenarios, execution, and reporting.

## Table of Contents

1. [Testing Framework](#testing-framework)
2. [Setup Instructions](#setup-instructions)
3. [Test Scenarios](#test-scenarios)
4. [Running Tests](#running-tests)
5. [Test Reports](#test-reports)
6. [CI/CD Integration](#cicd-integration)
7. [Troubleshooting](#troubleshooting)

---

## Testing Framework

### Technology Stack

- **Playwright**: Browser automation framework for E2E testing
- **Pytest**: Testing framework for organizing and running tests
- **pytest-html**: Generate HTML test reports
- **pytest-playwright**: Pytest plugin for Playwright integration

### Architecture

```
tests/
├── test_e2e_ui.py           # Main E2E test suite
├── conftest.py              # Pytest configuration and fixtures
├── pytest.ini               # Pytest settings
├── requirements-e2e.txt     # Test dependencies
├── run_e2e_tests.py         # Test runner script
└── reports/                 # Generated test reports
    └── e2e_test_report.html
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
# Navigate to tests directory
cd tests

# Install E2E testing dependencies
pip install -r requirements-e2e.txt

# Install Playwright browsers
python -m playwright install chromium
```

### 2. Start Application Servers

**Frontend Server:**
```bash
# Navigate to frontend directory
cd frontend

# Start simple HTTP server on port 8080
python -m http.server 8080
```

**Backend Server:**
```bash
# Navigate to project root
cd ..

# Start Flask backend on port 5000
python backend/app.py
```

### 3. Verify Setup

```bash
# Check if servers are running
curl http://localhost:8080
curl http://localhost:5000/health
```

---

## Test Scenarios

### Test Suite 1: Basic Functionality

#### Test 1: Home Page Load
- **Objective**: Verify home page loads correctly
- **Steps**:
  1. Navigate to index.html
  2. Verify page title
  3. Check main heading
  4. Verify navigation links
- **Expected**: Page loads with correct elements

#### Test 2: Navigation Links
- **Objective**: Verify all navigation links work
- **Steps**:
  1. Click each navigation link
  2. Verify correct page loads
- **Expected**: All links navigate to correct pages

#### Test 3: Form Validation
- **Objective**: Verify product input form validation
- **Steps**:
  1. Submit empty form
  2. Submit with invalid data
  3. Check for error messages
- **Expected**: Validation errors display correctly

### Test Suite 2: Core Workflow

#### Test 4: Complete Prediction Workflow
- **Objective**: Test end-to-end prediction workflow
- **Steps**:
  1. Fill product input form
  2. Submit form
  3. Wait for API response
  4. Verify results page loads
  5. Check recommendations table
- **Expected**: Full workflow completes successfully

#### Test 5: Analytics Without Data
- **Objective**: Verify analytics page handles no data
- **Steps**:
  1. Clear localStorage
  2. Navigate to analytics page
  3. Check for "No Data" message
- **Expected**: Proper message displayed, buttons disabled

#### Test 6: Analytics With Data
- **Objective**: Verify analytics dashboard displays correctly
- **Steps**:
  1. Generate prediction data
  2. Navigate to analytics
  3. Verify charts render
  4. Check data table
- **Expected**: All charts and data display correctly

### Test Suite 3: Export Functionality

#### Test 7: CSV Export
- **Objective**: Verify CSV export functionality
- **Steps**:
  1. Generate prediction data
  2. Navigate to analytics
  3. Click CSV export button
  4. Verify file download
- **Expected**: CSV file downloads with correct data

#### Test 8: PDF Export
- **Objective**: Verify PDF export functionality
- **Steps**:
  1. Generate prediction data
  2. Navigate to analytics
  3. Click PDF export button
  4. Verify file download
- **Expected**: PDF file downloads with correct formatting

### Test Suite 4: Error Handling

#### Test 9: API Error Handling
- **Objective**: Verify proper error handling when API fails
- **Steps**:
  1. Intercept API calls
  2. Simulate API failure
  3. Submit form
  4. Check error message
- **Expected**: Error message displays correctly

### Test Suite 5: Responsive Design

#### Test 10: Mobile Viewport
- **Objective**: Verify responsive design on mobile
- **Steps**:
  1. Set mobile viewport (375x667)
  2. Navigate through all pages
  3. Verify layout adapts
- **Expected**: All pages display correctly on mobile

### Test Suite 6: Data Persistence

#### Test 12: Cross-Page Data Persistence
- **Objective**: Verify data persists across navigation
- **Steps**:
  1. Generate prediction
  2. Navigate to different pages
  3. Return to analytics
  4. Verify data still available
- **Expected**: Data persists in localStorage

### Test Suite 7: Performance

#### Test 13: Page Load Time
- **Objective**: Verify acceptable page load times
- **Steps**:
  1. Measure page load time
  2. Verify < 3 seconds
- **Expected**: Pages load quickly

#### Test 14: Chart Rendering Performance
- **Objective**: Verify charts render efficiently
- **Steps**:
  1. Navigate to analytics with data
  2. Measure chart rendering time
  3. Verify < 5 seconds
- **Expected**: Charts render quickly

---

## Running Tests

### Run All Tests

```bash
# Using test runner script
python run_e2e_tests.py

# Using pytest directly
pytest test_e2e_ui.py -v --html=reports/e2e_test_report.html --self-contained-html
```

### Run Specific Test Classes

```bash
# Run only workflow tests
pytest test_e2e_ui.py::TestEcoPackAIWorkflow -v

# Run only performance tests
pytest test_e2e_ui.py::TestPerformance -v
```

### Run Specific Tests

```bash
# Run single test
pytest test_e2e_ui.py::TestEcoPackAIWorkflow::test_complete_prediction_workflow -v

# Run tests matching pattern
pytest test_e2e_ui.py -k "export" -v
```

### Run with Different Options

```bash
# Run in headless mode (no browser window)
pytest test_e2e_ui.py --headed=false

# Run with slow motion (for debugging)
pytest test_e2e_ui.py --slowmo=1000

# Run with video recording
pytest test_e2e_ui.py --video=on

# Run with screenshots on failure
pytest test_e2e_ui.py --screenshot=on
```

---

## Test Reports

### HTML Report

After running tests, an HTML report is generated at:
```
tests/reports/e2e_test_report.html
```

The report includes:
- Test execution summary
- Pass/fail status for each test
- Execution time
- Error messages and stack traces
- Screenshots (if enabled)

### Opening the Report

```bash
# Windows
start tests/reports/e2e_test_report.html

# Linux/Mac
open tests/reports/e2e_test_report.html
```

### Test Outputs

Additional test outputs are stored in:
```
tests/test_outputs/
├── screenshots/    # Screenshots of failures
├── downloads/      # Downloaded files from tests
└── videos/         # Video recordings (if enabled)
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r environments/requirements.txt
        pip install -r tests/requirements-e2e.txt
        python -m playwright install chromium
    
    - name: Start Backend Server
      run: |
        python backend/app.py &
        sleep 5
    
    - name: Start Frontend Server
      run: |
        cd frontend
        python -m http.server 8080 &
        sleep 3
    
    - name: Run E2E Tests
      run: |
        cd tests
        pytest test_e2e_ui.py -v --headed=false --html=reports/e2e_test_report.html
    
    - name: Upload Test Report
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: e2e-test-report
        path: tests/reports/
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Servers Not Running

**Error**: Connection refused or timeout errors

**Solution**:
```bash
# Check if ports are in use
netstat -an | findstr "8080"
netstat -an | findstr "5000"

# Start servers if not running
cd frontend && python -m http.server 8080
python backend/app.py
```

#### Issue 2: Playwright Not Installed

**Error**: "Executable doesn't exist"

**Solution**:
```bash
python -m playwright install chromium
```

#### Issue 3: Tests Timeout

**Error**: Tests timeout waiting for elements

**Solution**:
- Increase timeout in pytest.ini
- Check if servers are responding
- Verify network connectivity

#### Issue 4: Chart Tests Fail

**Error**: Charts not rendering in tests

**Solution**:
- Ensure Chart.js library is loaded
- Add wait time for chart rendering
- Check browser console for JavaScript errors

#### Issue 5: Download Tests Fail

**Error**: Download not detected

**Solution**:
- Verify browser download permissions
- Check download directory exists
- Ensure export buttons are enabled

### Debug Mode

Run tests in debug mode to see what's happening:

```bash
# Enable debug logging
pytest test_e2e_ui.py -v -s --log-cli-level=DEBUG

# Run with browser visible and slow motion
pytest test_e2e_ui.py --headed --slowmo=1000
```

### Viewing Test Screenshots

```bash
# Screenshots are saved on failure
# View them in test_outputs/screenshots/
```

---

## Best Practices

### Writing Tests

1. **Use descriptive test names**: Test names should clearly describe what is being tested
2. **Keep tests independent**: Each test should be able to run independently
3. **Clean up after tests**: Use fixtures to ensure proper setup and teardown
4. **Use explicit waits**: Wait for elements to be visible/ready before interacting
5. **Add meaningful assertions**: Verify expected outcomes clearly

### Test Maintenance

1. **Regular execution**: Run tests regularly to catch regressions early
2. **Update selectors**: Keep CSS selectors up to date with UI changes
3. **Review failures**: Investigate and fix failing tests promptly
4. **Monitor performance**: Track test execution times
5. **Update documentation**: Keep test documentation current

### Performance Optimization

1. **Parallel execution**: Run independent tests in parallel
2. **Reuse browser context**: Share browser instances where possible
3. **Minimize waits**: Use explicit waits instead of arbitrary delays
4. **Cache data**: Reuse test data when possible

---

## Test Coverage

### Current Coverage

- ✅ Home page functionality
- ✅ Navigation between pages
- ✅ Form validation
- ✅ Product input workflow
- ✅ Prediction API integration
- ✅ Results display
- ✅ Analytics charts rendering
- ✅ CSV export functionality
- ✅ PDF export functionality
- ✅ Error handling
- ✅ Responsive design
- ✅ Data persistence
- ✅ Performance metrics

### Future Coverage

- ⏳ Authentication flows (if implemented)
- ⏳ Multi-language support (if implemented)
- ⏳ Advanced analytics features
- ⏳ User preferences and settings

---

## Contact & Support

For questions or issues with the E2E testing framework:

1. Check this documentation
2. Review test code comments
3. Check test execution logs
4. Consult Playwright documentation: https://playwright.dev/python/

---

**Last Updated**: January 8, 2026
**Version**: 1.0.0
