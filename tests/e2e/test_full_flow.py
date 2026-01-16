from playwright.sync_api import sync_playwright

def test_full_ecopack_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://localhost:8000/")

        page.fill("#product_weight", "10")
        page.select_option("#material_type", "plastic")
        page.fill("#recyclability_score", "0.6")

        page.click("button[type=submit]")

        # ✅ wait for client-side redirect
        page.wait_for_url("**/results.html")

        # ✅ wait for JS-rendered rows
        page.wait_for_selector("#resultBody tr")

        rows = page.locator("#resultBody tr")
        assert rows.count() > 0

        browser.close()
