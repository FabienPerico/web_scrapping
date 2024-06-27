import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin")
        print(await page.title())
        await browser.close()
    print("test")

asyncio.run(main())