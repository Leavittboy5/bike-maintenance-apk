from playwright.sync_api import Page, expect, sync_playwright

def test_tire_physics(page: Page):
    # Load the local HTML file directly
    page.goto("file:///app/index.html")

    # The app stores data in localStorage, clear it
    page.evaluate("localStorage.clear()")
    page.reload()

    # Open Settings
    settings_button = page.locator("button[onclick='toggleSettings(true)']").first
    settings_button.click()

    # Set Weight to 120
    weight_input = page.locator("#settings-weight")
    weight_input.fill("120")
    weight_input.blur() # Trigger onchange/updateProfile

    # Close Settings
    close_settings = page.locator("button[onclick='toggleSettings(false)']")
    close_settings.click()

    # Wait a moment for modal animation
    page.wait_for_timeout(300)

    # Force evaluate the JS function directly since CSS positioning might block clicks in headless
    page.evaluate("selectHotspot('tires')")

    # Wait for the UI update
    page.wait_for_timeout(300)

    # Verify the widget is visible and contains expected math:
    # 120 (Rider) + 54 (Bike) + 10 (Gear) = 184
    # Wait, 184 means 180-200 range -> 26/29 Tubeless, 30/33 Tubes

    expect(page.locator("#tire-physics-widget")).to_be_visible()
    expect(page.locator("#tire-total-weight")).to_have_text("184")
    expect(page.locator("#tire-tubeless-psi")).to_have_text("26/29")
    expect(page.locator("#tire-tubes-psi")).to_have_text("30/33")

    page.screenshot(path="/app/verification/tire-physics.png", full_page=True)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Set a reasonable viewport
        page = browser.new_page(viewport={"width": 414, "height": 896})
        try:
            test_tire_physics(page)
        finally:
            browser.close()
