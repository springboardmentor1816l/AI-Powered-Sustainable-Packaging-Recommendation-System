"""
EcoPackAI - End-to-End UI Test Suite
Tests the complete user journey from product input to recommendation visualization
"""

import pytest
from playwright.sync_api import Page, expect
import json
import time
from pathlib import Path


class TestEcoPackAIWorkflow:
    """Test suite for EcoPackAI end-to-end workflows"""

    # Test configuration
    BASE_URL = "http://localhost:8080"  # Adjust based on your frontend server
    API_URL = "http://localhost:5000"   # Backend API endpoint
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup before each test"""
        page.set_viewport_size({"width": 1280, "height": 720})
        # Clear localStorage before each test
        page.goto(self.BASE_URL)
        page.evaluate("localStorage.clear()")
        yield page

    def test_home_page_loads(self, page: Page):
        """Test 1: Verify home page loads correctly"""
        page.goto(f"{self.BASE_URL}/index.html")
        
        # Check page title
        expect(page).to_have_title("EcoPackAI")
        
        # Check main heading
        heading = page.locator("h1")
        expect(heading).to_contain_text("EcoPackAI")
        
        # Check navigation links
        expect(page.locator("nav a")).to_have_count(3)
        
        print("✅ Home page loaded successfully")

    def test_navigation_links(self, page: Page):
        """Test 2: Verify all navigation links work"""
        page.goto(f"{self.BASE_URL}/index.html")
        
        # Test Product Input link
        page.click("text=Product Input")
        expect(page).to_have_url(f"{self.BASE_URL}/product.html")
        
        # Test Analytics link
        page.click("text=Analytics")
        expect(page).to_have_url(f"{self.BASE_URL}/analytics.html")
        
        # Test Home link
        page.click("text=Home")
        expect(page).to_have_url(f"{self.BASE_URL}/index.html")
        
        print("✅ All navigation links working")

    def test_product_input_form_validation(self, page: Page):
        """Test 3: Verify form validation on product input page"""
        page.goto(f"{self.BASE_URL}/product.html")
        
        # Try submitting empty form
        page.click("button[type='submit']")
        
        # Check for validation message (HTML5 required attribute)
        product_name_input = page.locator("#productName")
        expect(product_name_input).to_be_visible()
        
        # Fill in invalid weight
        page.fill("#productName", "Test Product")
        page.select_option("#category", "Food")
        page.fill("#weight", "-5")  # Invalid negative weight
        page.fill("#fragility", "5")
        page.select_option("#shipping", "Air")
        
        # Submit and check for error
        page.click("button[type='submit']")
        
        # Error message should appear
        error_msg = page.locator("#errorMsg")
        expect(error_msg).to_contain_text("Weight must be greater than 0")
        
        print("✅ Form validation working correctly")

    def test_complete_prediction_workflow(self, page: Page):
        """Test 4: Complete workflow from input to results"""
        page.goto(f"{self.BASE_URL}/product.html")
        
        # Fill in valid product details
        page.fill("#productName", "Organic Tea Box")
        page.select_option("#category", "Food")
        page.fill("#weight", "2.5")
        page.fill("#fragility", "7")
        page.select_option("#shipping", "Road")
        
        # Submit form
        page.click("button[type='submit']")
        
        # Check for loading indicator
        loading_msg = page.locator("#loadingMsg")
        expect(loading_msg).to_be_visible()
        
        # Wait for redirect to results page (with timeout)
        page.wait_for_url(f"{self.BASE_URL}/results.html", timeout=10000)
        
        # Verify results table is populated
        results_table = page.locator("#resultsTable tbody tr")
        expect(results_table.first).to_be_visible()
        
        # Check that at least one material recommendation is shown
        expect(results_table).to_have_count_greater_than(0)
        
        # Verify first row is highlighted (best recommendation)
        first_row = results_table.first
        background_color = first_row.evaluate("el => window.getComputedStyle(el).backgroundColor")
        assert "rgb(230, 244, 234)" in background_color or background_color != "rgba(0, 0, 0, 0)"
        
        print("✅ Complete prediction workflow successful")

    def test_analytics_dashboard_without_data(self, page: Page):
        """Test 5: Analytics page when no data is available"""
        page.goto(f"{self.BASE_URL}/analytics.html")
        
        # Should show "No Data Available" message
        no_data_msg = page.locator(".no-data-message")
        expect(no_data_msg).to_be_visible()
        expect(no_data_msg).to_contain_text("No Data Available")
        
        # Export buttons should be disabled
        csv_button = page.locator("#exportCSV")
        pdf_button = page.locator("#exportPDF")
        
        expect(csv_button).to_be_disabled()
        expect(pdf_button).to_be_disabled()
        
        print("✅ Analytics page correctly handles no data state")

    def test_analytics_dashboard_with_data(self, page: Page):
        """Test 6: Analytics dashboard displays charts and data"""
        # First, create a prediction to generate data
        page.goto(f"{self.BASE_URL}/product.html")
        
        page.fill("#productName", "Smartphone")
        page.select_option("#category", "Electronics")
        page.fill("#weight", "0.5")
        page.fill("#fragility", "9")
        page.select_option("#shipping", "Air")
        
        page.click("button[type='submit']")
        page.wait_for_url(f"{self.BASE_URL}/results.html", timeout=10000)
        
        # Now navigate to analytics
        page.click("text=Analytics")
        page.wait_for_url(f"{self.BASE_URL}/analytics.html")
        
        # Verify summary cards are present
        summary_cards = page.locator(".summary-card")
        expect(summary_cards).to_have_count(4)
        
        # Verify charts are rendered (canvas elements)
        cost_chart = page.locator("#costChart")
        co2_chart = page.locator("#co2Chart")
        sustainability_chart = page.locator("#sustainabilityChart")
        combined_chart = page.locator("#combinedChart")
        
        expect(cost_chart).to_be_visible()
        expect(co2_chart).to_be_visible()
        expect(sustainability_chart).to_be_visible()
        expect(combined_chart).to_be_visible()
        
        # Verify data table is populated
        table_rows = page.locator("#detailsTable tbody tr")
        expect(table_rows).to_have_count_greater_than(0)
        
        # Verify export buttons are enabled
        csv_button = page.locator("#exportCSV")
        pdf_button = page.locator("#exportPDF")
        
        expect(csv_button).to_be_enabled()
        expect(pdf_button).to_be_enabled()
        
        print("✅ Analytics dashboard displays correctly with data")

    def test_csv_export_functionality(self, page: Page):
        """Test 7: CSV export downloads correctly"""
        # Setup: Create prediction data
        page.goto(f"{self.BASE_URL}/product.html")
        
        page.fill("#productName", "Cosmetic Package")
        page.select_option("#category", "Cosmetics")
        page.fill("#weight", "1.0")
        page.fill("#fragility", "6")
        page.select_option("#shipping", "Sea")
        
        page.click("button[type='submit']")
        page.wait_for_url(f"{self.BASE_URL}/results.html", timeout=10000)
        
        # Navigate to analytics
        page.click("text=Analytics")
        page.wait_for_url(f"{self.BASE_URL}/analytics.html")
        
        # Wait for charts to load
        page.wait_for_timeout(1000)
        
        # Setup download listener
        with page.expect_download() as download_info:
            page.click("#exportCSV")
        
        download = download_info.value
        
        # Verify download happened
        assert download.suggested_filename.startswith("EcoPackAI_Report")
        assert download.suggested_filename.endswith(".csv")
        
        # Verify notification appears
        notification = page.locator(".export-notification")
        expect(notification).to_contain_text("CSV exported successfully")
        
        print("✅ CSV export functionality working")

    def test_pdf_export_functionality(self, page: Page):
        """Test 8: PDF export downloads correctly"""
        # Setup: Create prediction data
        page.goto(f"{self.BASE_URL}/product.html")
        
        page.fill("#productName", "Medicine Package")
        page.select_option("#category", "Pharmacy")
        page.fill("#weight", "0.3")
        page.fill("#fragility", "8")
        page.select_option("#shipping", "Air")
        
        page.click("button[type='submit']")
        page.wait_for_url(f"{self.BASE_URL}/results.html", timeout=10000)
        
        # Navigate to analytics
        page.click("text=Analytics")
        page.wait_for_url(f"{self.BASE_URL}/analytics.html")
        
        # Wait for charts to load
        page.wait_for_timeout(1000)
        
        # Setup download listener
        with page.expect_download() as download_info:
            page.click("#exportPDF")
        
        download = download_info.value
        
        # Verify download happened
        assert download.suggested_filename.startswith("EcoPackAI_Report")
        assert download.suggested_filename.endswith(".pdf")
        
        # Verify notification appears
        notification = page.locator(".export-notification")
        expect(notification).to_contain_text("PDF exported successfully")
        
        print("✅ PDF export functionality working")

    def test_api_error_handling(self, page: Page):
        """Test 9: Verify proper error handling when API fails"""
        # Stop the backend server or use wrong API endpoint
        page.goto(f"{self.BASE_URL}/product.html")
        
        # Intercept API calls and simulate failure
        page.route("**/predict", lambda route: route.abort())
        
        page.fill("#productName", "Test Product")
        page.select_option("#category", "Food")
        page.fill("#weight", "1.0")
        page.fill("#fragility", "5")
        page.select_option("#shipping", "Road")
        
        page.click("button[type='submit']")
        
        # Wait for error message
        page.wait_for_timeout(2000)
        
        api_error = page.locator("#apiError")
        expect(api_error).to_be_visible()
        expect(api_error).to_contain_text("Failed to fetch recommendations")
        
        print("✅ API error handling working correctly")

    def test_responsive_design_mobile(self, page: Page):
        """Test 10: Verify responsive design on mobile viewport"""
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        
        page.goto(f"{self.BASE_URL}/index.html")
        
        # Check that navigation is visible
        nav = page.locator("nav")
        expect(nav).to_be_visible()
        
        # Check that main content is visible
        main = page.locator("main")
        expect(main).to_be_visible()
        
        # Test form on mobile
        page.goto(f"{self.BASE_URL}/product.html")
        
        # Form should be visible and usable
        form = page.locator("#productForm")
        expect(form).to_be_visible()
        
        # Test analytics on mobile
        page.goto(f"{self.BASE_URL}/analytics.html")
        
        # Charts container should adapt to mobile
        charts_container = page.locator("#chartsContainer")
        expect(charts_container).to_be_visible()
        
        print("✅ Responsive design working on mobile viewport")

    def test_browser_compatibility_chrome(self, page: Page):
        """Test 11: Verify functionality in Chrome"""
        # This test will automatically run in Chrome by default
        page.goto(f"{self.BASE_URL}/index.html")
        
        # Test basic functionality
        expect(page).to_have_title("EcoPackAI")
        
        print("✅ Chrome browser compatibility verified")

    def test_data_persistence_across_pages(self, page: Page):
        """Test 12: Verify data persists across page navigation"""
        # Create prediction
        page.goto(f"{self.BASE_URL}/product.html")
        
        page.fill("#productName", "Test Product")
        page.select_option("#category", "Food")
        page.fill("#weight", "1.5")
        page.fill("#fragility", "5")
        page.select_option("#shipping", "Road")
        
        page.click("button[type='submit']")
        page.wait_for_url(f"{self.BASE_URL}/results.html", timeout=10000)
        
        # Navigate to home and back to analytics
        page.click("text=Home")
        page.click("text=Analytics")
        
        # Data should still be available
        summary_cards = page.locator(".summary-card")
        expect(summary_cards).to_have_count(4)
        
        print("✅ Data persistence across pages verified")


class TestPerformance:
    """Performance and load time tests"""

    BASE_URL = "http://localhost:8080"
    
    def test_page_load_time(self, page: Page):
        """Test 13: Verify page load times are acceptable"""
        start_time = time.time()
        page.goto(f"{self.BASE_URL}/index.html")
        load_time = time.time() - start_time
        
        # Page should load in less than 3 seconds
        assert load_time < 3.0, f"Page load time too slow: {load_time}s"
        
        print(f"✅ Page load time: {load_time:.2f}s")

    def test_chart_rendering_performance(self, page: Page):
        """Test 14: Verify charts render in reasonable time"""
        # Create prediction data
        page.goto(f"{self.BASE_URL}/product.html")
        
        page.fill("#productName", "Test")
        page.select_option("#category", "Food")
        page.fill("#weight", "1.0")
        page.fill("#fragility", "5")
        page.select_option("#shipping", "Road")
        
        page.click("button[type='submit']")
        page.wait_for_url(f"{self.BASE_URL}/results.html", timeout=10000)
        
        # Navigate to analytics and measure chart render time
        start_time = time.time()
        page.click("text=Analytics")
        
        # Wait for all charts to be visible
        page.wait_for_selector("#costChart", state="visible")
        page.wait_for_selector("#co2Chart", state="visible")
        page.wait_for_selector("#sustainabilityChart", state="visible")
        page.wait_for_selector("#combinedChart", state="visible")
        
        render_time = time.time() - start_time
        
        # Charts should render in less than 5 seconds
        assert render_time < 5.0, f"Chart rendering too slow: {render_time}s"
        
        print(f"✅ Chart rendering time: {render_time:.2f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=test_report.html", "--self-contained-html"])
