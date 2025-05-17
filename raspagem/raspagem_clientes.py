from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

# Caminho do chromedriver
chromedriver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"

# Configurações do navegador
servico = Service(chromedriver_path)
controle = webdriver.ChromeOptions()
controle.add_argument("--disable-gpu")
controle.add_argument("--window-size=1920,1080")
controle.add_argument("--headless")

executador = webdriver.Chrome(service=servico, options=controle)

url_site = 'https://masander.github.io/AlimenticiaLTDA/#/commercial'
executador.get(url_site)
time.sleep(3)

# Clicar no botão "Clientes"
try:
    botao_clientes = WebDriverWait(executador, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//nav/button[contains(text(), 'Clientes')]"))
    )
    executador.execute_script("arguments[0].click();", botao_clientes)
    time.sleep(3)
except Exception as e:
    print("Erro ao clicar no botão clientes:", e)
    executador.quit()
    exit()

# Iniciar dicionário
clientes = {
    'Id_cliente': [],
    'Nome': [],
    'Email': [],
    'Cidade': [],
    'Categoria': []
    
}

while True:
    print(f"\nColetando clientes da página...")

    try:
        linhas = WebDriverWait(executador, 10).until(
            ec.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr"))
        )
    except TimeoutException:
        print("Tempo de espera excedido!")
        break

    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        if len(colunas) == 5:
            clientes['Id_cliente'].append(colunas[0].text)
            clientes['Nome'].append(colunas[1].text)
            clientes['Email'].append(colunas[2].text)
            clientes['Cidade'].append(colunas[3].text)
            clientes['Categoria'].append(colunas[4].text)
    break

executador.quit()

# Exportar planilha
df_clientes = pd.DataFrame(clientes)
df_clientes.to_excel("C:/Users/49439967870/Desktop/Ciência_de_dados/Hackaton_17_05/raspagem/tabelas/tabela_clientes.xlsx", index=False)

print(f"Arquivo 'clientes.xlsx' salvo com sucesso! {len(df_clientes)} linhas coletadas!")