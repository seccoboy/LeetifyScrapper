from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time
import os

# Configurações do WebDriver
driver = webdriver.Chrome()  # Certifique-se de ter o ChromeDriver instalado e no PATH
wait = WebDriverWait(driver, 10)

# Acessa a página de login
driver.get("https://leetify.com/app/matches/list")

# Preenche campos de login
email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
email_field.send_keys("")

password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_field.send_keys("")

# Envia o formulário de login
password_field.send_keys(Keys.RETURN)

# Aguarda a página carregar
wait.until(EC.url_contains("/matches/list"))

# Name and Leetify IDs 
players = {
    "Name of the file": "aaaaaaaa-aaaa-cccc-ssss-123456789101"
}
# Percorre os jogadores e acessa suas respectivas páginas
for name, player_id in players.items():
    # Constrói a URL para acessar a página do jogador
    player_url = f"https://leetify.com/app/matches/list?spectating={player_id}"
    # Acessa a página do jogador
    driver.get(player_url)

    # Aguarda um tempo adicional para garantir que todos os elementos sejam carregados
    time.sleep(3)

    # Obtém o conteúdo HTML atualizado
    conteudo_atualizado = driver.page_source

    # Obtém o conteúdo HTML do elemento <body>
    body_content = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")

    # Analisa o conteúdo HTML do <body>
    soup = BeautifulSoup(body_content, 'html.parser')

    # Encontra todos os elementos app-matches-list-item
    items = soup.find_all('app-matches-list-item')

    # Percorre todos os elementos e extrai os links de partida
    links_partida = []
    for item in items:
        celula_link = item.find('a')
        if celula_link:
            link_partida = celula_link.get('href')
            links_partida.append(link_partida)
    time.sleep(2)

    tabela = soup.find('app-match-history-container', class_='ng-star-inserted')
    if tabela is not None:
        # Encontra as linhas da tabela
        linhas = tabela.find_all('tr')

        # Encontra o índice da coluna "Source" no cabeçalho
        cabecalho = linhas[0].find_all('th')
        indice_source = None
        for i, coluna in enumerate(cabecalho):
            if coluna.text.strip() == "Source":
                indice_source = i
                break

        if indice_source is not None:
            # Cria um arquivo CSV para escrita
            filename = f"parsed/{name}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as arquivo_csv:
                writer = csv.writer(arquivo_csv)

                # Escreve o cabeçalho do CSV
                cabecalho_csv = [coluna.text.strip() for coluna in cabecalho]
                cabecalho_csv.append("Link")  # Adiciona o cabeçalho da nova coluna
                writer.writerow(cabecalho_csv)

                # Itera pelas linhas e extrai os dados das células
                for i, linha in enumerate(linhas[1:], start=1):  # Começa da segunda linha para evitar o cabeçalho
                    # Encontra as células da linha
                    celulas = linha.find_all('td')

                    # Verifica se o índice da coluna "Source" existe na linha
                    if len(celulas) > indice_source:
                        # Extrai o conteúdo do atributo "alt" da imagem para obter o texto desejado
                        source = celulas[indice_source].find('img')['alt'].strip()
                    else:
                        source = ""

                    # Extrai o conteúdo das células da linha
                    dados = [celula.text.strip() for celula in celulas]

                    # Adiciona o valor da coluna "Source" aos dados
                    dados.append(source)

                    # Adiciona o link da partida aos dados
                    dados.append( links_partida[i - 1].split('?')[0])

                    # Escreve os dados no arquivo CSV
                    writer.writerow(dados)

            print(f"Dados do jogador {name} salvos no arquivo CSV: {filename}")
        else:
            print(f"Coluna 'Source' não encontrada na tabela do jogador {name}")
    else:
        print(f"Tabela do jogador {name} não encontrada")

os.system("python.exe remove_virgulas.py")
os.system("python.exe remove_blank_collumns.py")
