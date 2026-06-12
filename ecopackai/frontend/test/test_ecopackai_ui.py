from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

# 🔴 CHANGE THIS URL IF NEEDED
URL = "http://127.0.0.1:5500/product.html"
# If above does NOT load in browser, use:
# URL = "http://127.0.0.1:5500/frontend/product.html"

driver.get(URL)

# 🔒 HARD WAIT (prevents window auto-close)
time.sleep(3)

# ✅ WAIT FOR FORM
wait.until(EC.presence_of_element_located((By.ID, "productForm")))

# Fill form
driver.find_element(By.ID, "category").send_keys("Food")
driver.find_element(By.ID, "shipping_type").send_keys("Road")
driver.find_element(By.ID, "material_type").send_keys("PLA")
driver.find_element(By.ID, "packaging_type").send_keys("Box")
driver.find_element(By.ID, "supplier_region").send_keys("Asia")
driver.find_element(By.ID, "product_weight_kg").send_keys("1")
driver.find_element(By.ID, "fragility_index").send_keys("0.2")

# Submit
driver.find_element(By.TAG_NAME, "button").click()

# Wait for results page
wait.until(EC.presence_of_element_located((By.ID, "resultBody")))

assert "Sustainability Prediction Results" in driver.page_source

driver.save_screenshot("e2e_success.png")
driver.quit()

print("✅ E2E UI Test Passed Successfully")
