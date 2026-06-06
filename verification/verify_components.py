from playwright.sync_api import Page, expect, sync_playwright

def test_radar_and_garage(page: Page):
    # Load the local HTML file directly
    page.goto("file:///app/index.html")

    # The app stores data in localStorage, so let's clear it just in case
    page.evaluate("localStorage.clear()")
    page.reload()

    # Navigate to the Radar page
    radar_button = page.locator("button[onclick=\"switchTab('tab-reports')\"]")
    radar_button.click()

    # Verify the Radar tab is active and visible
    expect(page.locator("#tab-reports")).not_to_have_class("hidden")

    # Verify a couple of the new default components are listed on the radar page
    expect(page.locator("#radar-container")).to_contain_text("Tires: Check damage/inflate")
    expect(page.locator("#radar-container")).to_contain_text("Brakes: Check levers")

    # Take a screenshot of the radar page
    page.screenshot(path="/app/verification/radar-page.png", full_page=True)

    # Navigate to the Garage page
    garage_button = page.locator("button[onclick=\"switchTab('tab-garage')\"]")
    garage_button.click()

    # Verify the new checklist items are present in the garage
    expect(page.locator("#garage-checklist")).to_contain_text("Tires: Check damage/inflate (20-40 PSI)")
    expect(page.locator("#garage-checklist")).to_contain_text("Brakes: Ensure firm levers")

    # Take a screenshot of the garage page
    page.screenshot(path="/app/verification/garage-page.png", full_page=True)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Set a reasonable viewport for testing a mobile/responsive layout
        page = browser.new_page(viewport={"width": 414, "height": 896})
        try:
            test_radar_and_garage(page)
        finally:
            browser.close()
