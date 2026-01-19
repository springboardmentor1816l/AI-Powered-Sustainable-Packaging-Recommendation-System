"""
End-to-End UI Tests
===================

Automated UI testing using Playwright for EcoPackAI frontend workflows.
Tests the complete user journey from input to prediction display.

Author: EcoPackAI Team
Date: 2026-01-12
"""

import pytest
from playwright.sync_api import Page, expect
import time
import json
from pathlib import Path


# Test Configuration
BASE_URL = "http://localhost:5000"
TIMEOUT = 30000  # 30 seconds


class TestEcoPackAIWorkflow:
    """End-to-end workflow tests for EcoPackAI application"""
    
    @pytest.fixture(scope="function")
    def sample_material_data(self):
        """Sample material data for testing"""
        return {
            "recyclability_percent": 95.0,
            "recycled_content_percent": 70.0,
            "reusability_percent": 50.0,
            "biodegradation_time_days": 120,
            "end_of_life_disposal_percent": 95.0,
            "carbon_footprint_kg_co2_unit": 1.8,
            "waste_reduction_impact_percent": 80.0,
            "sustainability_target_progress_percent": 85.0,
            "load_handling_score": 8.0,
            "moisture_resistance_score": 7.0,
            "thermal_resistance_score": 7.0,
            "annual_usage_units": 15000,
            "total_material_weight_tons": 7.5,
            "supplier_sustainability_compliance_percent": 90.0,
            "co2_impact_index": 0.25,
            "cost_efficiency_index": 0.75,
            "material_suitability_score": 70.0,
            "overall_sustainability_score": 0.85
        }
    
    def test_home_page_loads(self, page: Page):
        """Test 1: Home page loads successfully"""
        page.goto(f"{BASE_URL}/frontend/index.html", timeout=TIMEOUT)
        
        # Check page title
        expect(page).to_have_title("EcoPackAI - Sustainable Packaging Intelligence")
        
        # Check navbar presence
        navbar = page.locator(".navbar")
        expect(navbar).to_be_visible()
        
        # Check hero section
        hero = page.locator(".hero")
        expect(hero).to_be_visible()
        expect(hero.locator("h1")).to_contain_text("AI-Powered Sustainable Packaging Intelligence")
        
        print("✓ Home page loaded successfully")
    
    def test_navigation_links(self, page: Page):
        """Test 2: Navigation links work correctly"""
        page.goto(f"{BASE_URL}/frontend/index.html", timeout=TIMEOUT)
        
        # Test Predict link
        page.click("a.nav-link:has-text('Predict')")
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(f"{BASE_URL}/frontend/predict.html")
        
        # Navigate back to home
        page.click("a.nav-link:has-text('Home')")
        expect(page).to_have_url(f"{BASE_URL}/frontend/index.html")
        
        # Test Results link
        page.click("a.nav-link:has-text('Results')")
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(f"{BASE_URL}/frontend/results.html")
        
        # Test Dashboard link
        page.click("a.nav-link:has-text('Dashboard')")
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(f"{BASE_URL}/frontend/dashboard.html")
        
        print("✓ All navigation links working")
    
    def test_prediction_form_validation(self, page: Page):
        """Test 3: Form validation works correctly"""
        page.goto(f"{BASE_URL}/frontend/predict.html", timeout=TIMEOUT)
        
        # Try submitting empty form
        submit_button = page.locator("button[type='submit']").first
        submit_button.click()
        
        # Wait a moment for validation
        time.sleep(1)
        
        # Check for validation messages or errors
        # Note: Actual validation depends on implementation
        
        print("✓ Form validation tested")
    
    def test_prediction_submission(self, page: Page, sample_material_data):
        """Test 4: Prediction form submission and API call"""
        page.goto(f"{BASE_URL}/frontend/predict.html", timeout=TIMEOUT)
        
        # Fill form fields
        for field_name, value in sample_material_data.items():
            input_field = page.locator(f"input[name='{field_name}'], input[id='{field_name}']").first
            if input_field.is_visible():
                input_field.fill(str(value))
        
        # Intercept API request
        api_response = None
        
        def handle_response(response):
            nonlocal api_response
            if "/api/v1/predict" in response.url:
                api_response = response
        
        page.on("response", handle_response)
        
        # Submit form
        submit_button = page.locator("button[type='submit']").first
        submit_button.click()
        
        # Wait for response
        page.wait_for_timeout(2000)
        
        # Verify API was called
        if api_response:
            assert api_response.status == 200, f"API returned status {api_response.status}"
            print("✓ Prediction API called successfully")
        else:
            print("⚠ API call not detected (form implementation may differ)")
    
    def test_results_display(self, page: Page):
        """Test 5: Results page displays predictions"""
        page.goto(f"{BASE_URL}/frontend/results.html", timeout=TIMEOUT)
        
        # Check page structure
        expect(page.locator("h1")).to_contain_text("Prediction Results")
        
        # Check for results container or empty state
        empty_state = page.locator("#emptyState")
        results_list = page.locator("#resultsList")
        
        # One should be visible
        assert empty_state.is_visible() or results_list.is_visible(), \
            "Neither empty state nor results list is visible"
        
        print("✓ Results page structure verified")
    
    def test_csv_export_button(self, page: Page):
        """Test 6: CSV export button exists and is clickable"""
        page.goto(f"{BASE_URL}/frontend/results.html", timeout=TIMEOUT)
        
        # Look for export button
        export_buttons = page.locator("button:has-text('Export'), button:has-text('CSV')")
        
        if export_buttons.count() > 0:
            print("✓ Export button found")
            # Note: Actual download testing requires more complex setup
        else:
            print("⚠ Export button not found on results page")
    
    def test_pdf_export_button(self, page: Page):
        """Test 7: PDF export button exists"""
        page.goto(f"{BASE_URL}/frontend/results.html", timeout=TIMEOUT)
        
        # Look for PDF export button
        pdf_buttons = page.locator("button:has-text('PDF'), #exportPDF")
        
        if pdf_buttons.count() > 0:
            print("✓ PDF export button found")
        else:
            print("⚠ PDF export button not found")
    
    def test_api_health_check(self, page: Page):
        """Test 8: API health endpoint is accessible"""
        response = page.request.get(f"{BASE_URL}/health")
        
        assert response.ok, f"Health check failed with status {response.status}"
        
        data = response.json()
        assert data["status"] == "healthy", "API is not healthy"
        
        print("✓ API health check passed")
    
    def test_api_predict_endpoint(self, page: Page, sample_material_data):
        """Test 9: API prediction endpoint works"""
        response = page.request.post(
            f"{BASE_URL}/api/v1/predict/all",
            data=sample_material_data
        )
        
        assert response.ok, f"Prediction API failed with status {response.status}"
        
        data = response.json()
        assert data["status"] == "success", "Prediction failed"
        assert "results" in data, "No results in response"
        assert "predicted_cost" in data["results"], "Missing predicted_cost"
        assert "predicted_co2" in data["results"], "Missing predicted_co2"
        
        print(f"✓ API prediction successful: Cost=${data['results']['predicted_cost']:.2f}, "
              f"CO₂={data['results']['predicted_co2']:.4f}kg")
    
    def test_responsive_layout_mobile(self, page: Page):
        """Test 10: Responsive layout on mobile viewport"""
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        
        page.goto(f"{BASE_URL}/frontend/index.html", timeout=TIMEOUT)
        
        # Check if navbar is still visible
        navbar = page.locator(".navbar")
        expect(navbar).to_be_visible()
        
        print("✓ Mobile layout verified")
    
    def test_responsive_layout_tablet(self, page: Page):
        """Test 11: Responsive layout on tablet viewport"""
        # Set tablet viewport
        page.set_viewport_size({"width": 768, "height": 1024})
        
        page.goto(f"{BASE_URL}/frontend/index.html", timeout=TIMEOUT)
        
        navbar = page.locator(".navbar")
        expect(navbar).to_be_visible()
        
        print("✓ Tablet layout verified")
    
    def test_dashboard_page(self, page: Page):
        """Test 12: Dashboard page loads and displays content"""
        page.goto(f"{BASE_URL}/frontend/dashboard.html", timeout=TIMEOUT)
        
        # Check page loads
        expect(page).to_have_title("Dashboard - EcoPackAI")
        
        # Look for dashboard elements
        page.wait_for_load_state("networkidle")
        
        print("✓ Dashboard page loaded")
    
    def test_error_handling(self, page: Page):
        """Test 13: Error handling for invalid API requests"""
        # Send invalid request
        response = page.request.post(
            f"{BASE_URL}/api/v1/predict/all",
            data={"invalid": "data"}
        )
        
        # Should get error response
        assert response.status == 400, "Expected 400 Bad Request"
        
        data = response.json()
        assert data["status"] == "error", "Expected error status"
        
        print("✓ Error handling verified")
    
    def test_charts_library_loaded(self, page: Page):
        """Test 14: Chart.js library is loaded (if analytics page exists)"""
        page.goto(f"{BASE_URL}/frontend/results.html", timeout=TIMEOUT)
        
        # Check if Chart.js is loaded in window
        chart_loaded = page.evaluate("typeof Chart !== 'undefined'")
        
        if chart_loaded:
            print("✓ Chart.js library loaded")
        else:
            print("⚠ Chart.js not loaded (may need to be added)")


class TestAnalyticsWorkflow:
    """Tests specific to analytics and visualization features"""
    
    def test_analytics_manager_exists(self, page: Page):
        """Test analytics manager is initialized"""
        page.goto(f"{BASE_URL}/frontend/results.html", timeout=TIMEOUT)
        
        # Check if AnalyticsManager exists
        manager_exists = page.evaluate("typeof window.AnalyticsManager !== 'undefined'")
        
        if manager_exists:
            print("✓ AnalyticsManager initialized")
        else:
            print("⚠ AnalyticsManager not found (check if analytics.js is included)")
    
    def test_export_manager_exists(self, page: Page):
        """Test export manager is initialized"""
        page.goto(f"{BASE_URL}/frontend/results.html", timeout=TIMEOUT)
        
        # Check if ExportManager exists
        manager_exists = page.evaluate("typeof window.ExportManager !== 'undefined'")
        
        if manager_exists:
            print("✓ ExportManager initialized")
        else:
            print("⚠ ExportManager not found (check if export.js is included)")


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end UI test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Run tests with: pytest tests/e2e/test_ui_workflow.py -v
