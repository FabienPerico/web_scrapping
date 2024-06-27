from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin")
    page.screenshot(path="demo.png")
    browser.close()