from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import csv
import os

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
    time.sleep(2)
    
    try:
        wait = WebDriverWait(driver, 10)
        # Localiza e clica no botão "Match Details"
        match_details_button = driver.find_element(By.XPATH, '//a[text()="Match Details"]')
        match_details_button.click()

        # Espera até que a página de "Match Details" esteja carregada
        wait.until(EC.url_contains("/details-general"))

        # Localiza o menu de detalhes do jogo
        match_details_menu = driver.find_element(By.CLASS_NAME, "match-details-menu")
        csv_filename = link.split('/')[2]

        # Remove caracteres inválidos do nome do arquivo
        csv_filename = ''.join(c for c in csv_filename if c.isalnum() or c in ['-', '_'])

        # Caminho completo para o arquivo CSV
        csv_filepath = os.path.join('matches/', csv_filename + '.csv')
        csv_file = open(csv_filepath, 'w', newline='', encoding='utf-8')
        writer = csv.writer(csv_file)

        # Clica em cada item do submenu
        submenus = match_details_menu.find_elements(By.TAG_NAME, "a")
        for submenu in submenus:
            # Obtém o nome do submenu
            submenu_name = submenu.text.strip()
            if submenu_name not in ["General","Timeline", "Match Details","Trades", "Opening Duels","Clutches"]:
                # Localiza a tabela pelo XPath
                table = driver.find_element(By.XPATH, '//table[contains(@class, "--collapsed --use-min-width")]')

                # Localiza o cabeçalho da tabela
                header_row = table.find_element(By.TAG_NAME, 'thead')
                header_cells = header_row.find_elements(By.TAG_NAME, 'th')

                # Extrai o texto dos cabeçalhos
                header_data = [header_cell.text for header_cell in header_cells]
                # Escreve os cabeçalhos no arquivo CSV (apenas uma vez)
                writer.writerow(header_data)

                # Obtém o HTML da tabela
                table_html = table.get_attribute('outerHTML')

                # Parseia a tabela usando BeautifulSoup
                soup = BeautifulSoup(table_html, 'html.parser')

                # Obtém todas as linhas da tabela
                rows = soup.find_all('tr')

                # Loop através das linhas e extrai os dados das células
                for row in rows:
                    cells = row.find_all('td')
                    row_data = [cell.get_text(strip=True) for cell in cells]

                    # Escreve a linha no arquivo CSV
                    writer.writerow(row_data)

                # Move o cursor do mouse para o submenu
                ActionChains(driver).move_to_element(submenu).perform()
                
                # Clica no submenu
                submenu.click()

                # Espera até que a página do submenu esteja carregada
                submenu_url = "/details-" + submenu_name.lower().replace(" ", "-")
                wait.until(EC.url_contains(submenu_url))
                
        # Fecha o arquivo CSV
        csv_file.close()
        
    except Exception as e:
        print("Erro ao navegar pelos submenus:", str(e))
        continue
    
# Close the browser
driver.quit()

os.system("python.exe fix_csvs.py")