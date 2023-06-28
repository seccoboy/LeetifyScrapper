from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import csv
import os

def replace_text(text):
    return text.replace("Winning Team\nWIN", "Player")

# Initialize Selenium webdriver
driver = webdriver.Chrome()  # Replace with the appropriate webdriver for your browser

# Read the links from "links.txt"
with open("links.txt", "r") as file:
    links = file.read().splitlines()

# Loop through each link
for link in links:
    full_link = "https://leetify.com" + link
    
    # Open the link in the browser
    driver.get(full_link)
    time.sleep(5)
    
    try:
        wait = WebDriverWait(driver, 10)
        # Localiza e clica no botão "Match Details"
        match_details_button = driver.find_element(By.XPATH, '//a[text()="Match Details"]')
        match_details_button.click()

        # Espera até que a página de "Match Details" esteja carregada
        wait.until(EC.url_contains("/details-general"))

        # Localiza o menu de detalhes do jogo
        match_details_menu = driver.find_element(By.CLASS_NAME, "match-details-menu")
        csv_filename = link.split('/')[3]

        # Remove caracteres inválidos do nome do arquivo
        csv_filename = ''.join(c for c in csv_filename if c.isalnum() or c in ['-', '_'])

        # Loop through each submenu
        submenus = match_details_menu.find_elements(By.TAG_NAME, "a")
        for submenu in submenus:
            submenu_name = submenu.text.strip()
            if submenu_name not in ["Activity", "Timeline", "Match Details", "Trades", "Opening Duels", "Clutches"]:
                # Create a folder for the submenu
                folder_name = submenu_name.lower().replace(" ", "_")
                folder_path = os.path.join('matches', folder_name)
                os.makedirs(folder_path, exist_ok=True)

                # Create the CSV file inside the submenu folder
                csv_filepath = os.path.join(folder_path, csv_filename + '.csv')
                csv_file = open(csv_filepath, 'w', newline='', encoding='utf-8')
                writer = csv.writer(csv_file)

                # Click on the submenu
                ActionChains(driver).move_to_element(submenu).perform()
                submenu.click()

                # Wait until the submenu page is loaded
                submenu_url = "/details-" + submenu_name.lower().replace(" ", "-")
                wait.until(EC.url_contains(submenu_url))

                # Find the table by XPath
                table = driver.find_element(By.XPATH, '//table[contains(@class, "--collapsed --use-min-width")]')

                # Find the table header
                header_row = table.find_element(By.TAG_NAME, 'thead')
                header_cells = header_row.find_elements(By.TAG_NAME, 'th')

                # Extract the text from the header cells and replace the desired text
                header_data = [replace_text(header_cell.text) for header_cell in header_cells]
                # Write the headers to the CSV file (only once)
                writer.writerow(header_data)

                # Get the HTML of the table
                table_html = table.get_attribute('outerHTML')

                # Parse the table using BeautifulSoup
                soup = BeautifulSoup(table_html, 'html.parser')

                # Find all rows in the table
                rows = soup.find_all('tr')

                # Loop through the rows and extract cell data
                for row in rows:
                    cells = row.find_all('td')
                    row_data = [replace_text(cell.get_text(strip=True)) for cell in cells]
                    # Write the row to the CSV file
                    writer.writerow(row_data)

                # Close the CSV file
                csv_file.close()
                time.sleep(2)

    except Exception as e:
        print("Error navigating submenus:", str(e))
        continue

# Close the browser
driver.quit()
