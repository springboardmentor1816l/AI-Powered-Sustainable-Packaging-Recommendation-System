from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os

CHROMEDRIVER_PATH = os.path.join(
    os.path.dirname(__file__), "chromedriver.exe"
)

PREDICT_URL = "http://127.0.0.1:5501/predict.html"


def test_ui_prediction():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(PREDICT_URL)

        # ✅ Wait for form fields
        weight = wait.until(EC.presence_of_element_located((By.ID, "weight")))
        fragility = driver.find_element(By.ID, "fragility")
        shipping_dropdown = Select(driver.find_element(By.ID, "shipping"))

        # ✅ Fill form
        weight.clear()
        weight.send_keys("12")

        fragility.clear()
        fragility.send_keys("3")

        shipping_dropdown.select_by_visible_text("Local")

        # ✅ Click the Predict button safely
        predict_button = driver.find_element(
            By.XPATH, "//button[contains(text(),'Predict')]"
        )
        predict_button.click()

        # ✅ Wait for result
        result = wait.until(
            EC.presence_of_element_located((By.ID, "recScore"))
        )

        assert "Suitability Score" in result.text

    finally:
        driver.quit()
