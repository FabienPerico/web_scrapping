import asyncio
import csv
from playwright.async_api import async_playwright
# Load time's library, contain some timing function (sleep,wait...)
import time

async def login_to_linkedin(page, username, password):
    await page.goto('https://www.linkedin.com/login')

    await page.fill('input#username', username)
    await page.fill('input#password', password)
    await page.click('button[type="submit"]')

    # Attendre que la page se charge
    await page.wait_for_load_state('networkidle')

async def extract_profile_urls(page, search_query):
    search_url = f'https://www.linkedin.com/search/results/people/?keywords={search_query}'
    await page.goto(search_url)
    # time.sleep(20)

    # Attendre que les résultats de recherche se chargent
    await page.wait_for_selector('.reusable-search__result-container')

    # Extraire les URLs des profils
    profile_urls = []
    profiles = await page.query_selector_all('.reusable-search__result-container .entity-result__title-text a')
    for profile in profiles:
        url = await profile.get_attribute('href')
        if url and 'linkedin.com/in/' in url:
            profile_urls.append(url.split('?')[0])  # Enlever les paramètres de suivi

    return profile_urls

async def main(username, password, search_query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await login_to_linkedin(page, username, password)
        profile_urls = await extract_profile_urls(page, search_query)

        await browser.close()
        return profile_urls

def save_to_csv(data, filename='linkedin_profiles.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Profile URL'])  # Écrire l'en-tête
        for url in data:
            writer.writerow([url])  # Écrire les URLs dans le fichier

username = 'fabien.perico@apside.com'
password = '.5ri7?bZ#G+e+qH'
search_query = 'P'

profile_urls = asyncio.run(main(username, password, search_query))
save_to_csv(profile_urls)

print(f'Saved {len(profile_urls)} profile URLs to linkedin_profiles.csv')