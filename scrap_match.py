from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

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

        # Clica em cada item do submenu
        submenus = match_details_menu.find_elements(By.TAG_NAME, "a")
        for submenu in submenus:
            # Obtém o nome do submenu
            submenu_name = submenu.text.strip()
            if submenu_name not in ["General", "Match Details"]:
                # Move o cursor do mouse para o submenu
                ActionChains(driver).move_to_element(submenu).perform()
                
                # Clica no submenu
                submenu.click()

                # Espera até que a página do submenu esteja carregada
                submenu_url = "/details-" + submenu_name.lower().replace(" ", "-")
                wait.until(EC.url_contains(submenu_url))
        
    except Exception as e:
        print("Erro ao navegar pelos submenus:", str(e))
        continue
    
# Close the browser
driver.quit()
