from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def run_e2e_test():
    # Initialize the driver (Chrome example)
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        # 1. Test Home to Form Navigation
        driver.get("http://127.0.0.1:5000/")
        driver.find_element(By.LINK_TEXT, "Get Started").click()
        
        # 2. Test Form Submission
        driver.find_element(By.NAME, "category").send_keys("Electronics")
        driver.find_element(By.NAME, "weight").send_keys("1.5")
        driver.find_element(By.NAME, "fragility").send_keys("0.4")
        driver.find_element(By.ID, "predictionForm").submit()
        
        # 3. Validate Results Table Rendering
        time.sleep(2) # Wait for ML processing
        assert "AI-Powered Packaging Recommendations" in driver.page_source
        rows = driver.find_elements(By.TAG_NAME, "tr")
        assert len(rows) > 1 # Ensure table is not empty
        
        # 4. Validate Analytics Dashboard
        driver.get("http://127.0.0.1:5000/analytics")
        time.sleep(1)
        chart = driver.find_element(By.ID, "impactChart")
        assert chart.is_displayed()
        
        print("✅ All E2E Test Scenarios Passed!")
        
    except Exception as e:
        print(f"❌ Test Failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_e2e_test()