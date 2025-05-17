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

# Clicar no botão "Produtos"
try:
    botao_produtos = WebDriverWait(executador, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//nav/button[contains(text(), 'Produtos')]"))
    )
    executador.execute_script("arguments[0].click();", botao_produtos)
    time.sleep(3)
except Exception as e:
    print("Erro ao clicar no botão Produtos:", e)
    executador.quit()
    exit()

# Iniciar dicionário
produtos = {
    'Id_produto': [],
    'Nome_produto': [],
    'Categoria': [],
    'Preco_unitario': [],
    'Estoque_atual': []
    
}

while True:
    print(f"\nColetando produtos da página...")

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
            produtos['Id_produto'].append(colunas[0].text)
            produtos['Nome_produto'].append(colunas[1].text)
            produtos['Categoria'].append(colunas[2].text)
            produtos['Preco_unitario'].append(colunas[3].text)
            produtos['Estoque_atual'].append(colunas[4].text)
    break

executador.quit()

# Exportar planilha
df_produtos = pd.DataFrame(produtos)
df_produtos.to_excel("C:/Users/49439967870/Desktop/Ciência_de_dados/Hackaton_17_05/raspagem/tabelas/produtos.xlsx", index=False)

print(f"Arquivo 'produtos.xlsx' salvo com sucesso! {len(df_produtos)} linhas coletadas!")