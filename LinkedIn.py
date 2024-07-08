# Load asyncio's library, used for asynchronous api like here
import asyncio
# Load time's library, contain some timing function (sleep,wait...)
import time
# Load sys's library, contain some basic function
import sys
# Load Functionality used to drive the keyboard
import keyboard
# Load playwright's library to browse the Web
from playwright.async_api import async_playwright
# Load library to navagate in os file
import os
# Load library to hide the password
import getpass

async def login(page):
        # Open the page on LinkedIn Identification URL
        
        await page.goto("https://www.linkedin.com/checkpoint/rm/sign-in-another-account")
        # Interact with login form
        time.sleep(1)
        await page.fill('input#username', 'fabien.perico@apside.com')
        time.sleep(1)
        await page.fill('input#password', '.5ri7?bZ#G+e+qH')
        time.sleep(1)
        # Try to log
        await page.click('button[type=submit]')
        time.sleep(10)


async def search(page):
        # Initialisation of the parameter
        param=sys.argv[1]
        # Addition of other parameters available
        for strParam in sys.argv[2:]:
            # Concatenation of all parameters with ' '
            param = strParam + ' ' + param
        # Copy parameters in Search bar
        await page.get_by_role('combobox').fill(param)
        # Use the keybord to validate the request
        keyboard.press_and_release('enter')
        time.sleep(20)
        # Filter by people
        await page.get_by_role('button', name='Personnes').click()


async def extract_profile_urls(page):

    # wait for the result
    await page.wait_for_selector('.reusable-search__result-container')

    # Extract profil url
    profile_urls = []
    # Select result
    profiles = await page.query_selector_all('.reusable-search__result-container .entity-result__title-text a')
    # Parse all the result profile
    for profile in profiles:
        # Select url with the attribute 'href'
        url = await profile.get_attribute('href')
        # Verify if the link correspond the to people and not an advice
        if url and 'linkedin.com/in/' in url:
            # Delete the traking parameters
            profile_urls.append(url.split('?')[0])

    return profile_urls

def save_to_csv(data, filename='linkedin_profiles.csv'):
    with open(filename, mode='w', newline='') as file:
        # Create new csv file
        writer = csv.writer(file)
        # Write the header file
        writer.writerow(['Profile URL'])
        for url in data:
            # Write each Url
            writer.writerow([url])

async def main(username, password, search_query):
    async with async_playwright() as p:

        # Start new chromium session
        browser = await p.chromium.launch(headless=False)
        # start new page
        page = await browser.new_page()

        # Call login Api
        await login(page)
        time.sleep(60)
        # Call search Api
        await search(page)
        time.sleep(80)
        # Extrat profil url with extract_profile_urls Api
        profile_urls = await extract_profile_urls(page)
        
        # # Go to next page
        await page.get_by_role('button', name='Page 2').click()
        time.sleep(30)
        # # Extrat profil url with extract_profile_urls Api
        # profile_urls = await extract_profile_urls(page)
        

        # Close the page
        await browser.close()
        return profile_urls


username = 'fabien.perico@apside.com'
password = '.5ri7?bZ#G+e+qH'
search_query = 'emilie'

# Call the main Api
profile_urls = asyncio.run(main(username, password, search_query))
# Save the data in csv file
save_to_csv(profile_urls)