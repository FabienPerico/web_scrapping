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
# Load library to use .csv file
import csv
# Load library to navagate in os file
import os
# Load library to hide the password
import getpass


# This Api is used to save the username
def user(userfile):

    # Ask to the user for the username
    username = input("Veuillez entrer votre adresse email : ")

    # Save it in new file
    with open(userfile, 'w') as fichier:
        fichier.write(username)

    print("Adresse email enregistrée avec succès.")


# This Api is used to log an account
async def login(page, userfile):
        
        with open(userfile, 'r') as fichier:

            # Get the username in the file
            email = fichier.read().strip()

            # Open the page on LinkedIn Identification URL
            await page.goto("https://www.linkedin.com/checkpoint/rm/sign-in-another-account")

            # Interact with username
            await page.fill('input#username', email)
            # time.sleep(1)
            
            # Get the password hiden
            password = getpass.getpass("entrez votre mot de passe\n")
        
            # Interact with password
            await page.fill('input#password', password)
            # time.sleep(1)

            # Try to log
            await page.click('button[type=submit]')
            # time.sleep(2)


# This Api is used to start a filter by word(s)
async def search(page, param):
        
        # Copy parameters in Search bar
        await page.get_by_role('combobox').fill(param)

        # Cliquer sur le bouton de recherche
        await page.press('input[placeholder="Recherche"]', 'Enter')

        # Filter by people
        await page.get_by_role('button', name='Personnes').click()


# This Api is used to extract url of profiles (return profiles)
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



# This Api is used to save urls in .csv file
def save_to_csv(data, filename):

    with open(filename, mode='a', newline='') as file:

        # Create new csv file
        writer = csv.writer(file)

        for url in data:
            # Write each Url
            writer.writerow([url])


async def main():

    async with async_playwright() as p:
        # Start new chromium session
        browser = await p.chromium.launch(headless=True)

        # Start new page
        page = await browser.new_page()

        # Chemin du fichier à vérifier
        userfile = 'utilisateur.txt'

        # Vérify if the file already exist
        if os.path.exists('chemin_fichier'):
            # Call login Api
            await login(page, userfile)
        else:
            # Save the username
            user(userfile)
            # Call login Api
            await login(page, userfile)

        another="y"

        while another!="n":

            # Get the search parameter
            param = input("Que cherchez-vous?\n")

            # Get the number of the page will scrap
            pagenum = input("Sur combien de page (10 profils par page)?\n")

            # Call search Api
            await search(page,param)
            # time.sleep(2)

            # Extrat profil url with extract_profile_urls Api
            profile_urls = await extract_profile_urls(page)

            # Create the .csv filename to fill
            filename=param

            # Add extension name
            filename=filename+'.csv'

            # Verify if the file already exist
            if os.path.exists(filename):
                # If the file exist, the file will be remove
                os.remove(filename)

            # Initialise first page to 1
            url=1

            while url < (int(pagenum)+1):

                # Fill the .csv file with data
                save_to_csv(profile_urls, filename)

                # Increment the number of the page scrapped
                url = url+1

                # Scroll to the down of the page
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

                # Got to next page
                next_button_selector = 'button[aria-label="Suivant"]'
                await page.click(next_button_selector)

                # Wait for the result
                await page.wait_for_selector('.search-results-container', timeout=10000)
                profile_urls = await extract_profile_urls(page)
            
            # Ask if user have another request
            another = input("avez-vous une autre recherche? y or n\n")

        # Close the page
        await browser.close()

# Call the main Api
asyncio.run(main())