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

# Clicar no botão "vendas"
try:
    botao_vendas = WebDriverWait(executador, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//nav/button[contains(text(), 'Vendas')]"))
    )
    executador.execute_script("arguments[0].click();", botao_vendas)
    time.sleep(3)
except Exception as e:
    print("Erro ao clicar no botão vendas:", e)
    executador.quit()
    exit()

# Iniciar dicionário
vendas = {
    'Id_venda': [],
    'Id_cliente': [],
    'Id_Produto': [],
    'Data_venda': [],
    'Quantidade': [],
    'Valor_total': [],
    'Pedidos_concluido': [],
    'Avaliacao_servico': []
    
    
}

while True:
    print(f"\nColetando vendas da página...")

    try:
        linhas = WebDriverWait(executador, 10).until(
            ec.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr"))
        )
    except TimeoutException:
        print("Tempo de espera excedido!")
        break

    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        if len(colunas) == 8:
            vendas['Id_venda'].append(colunas[0].text)
            vendas['Id_cliente'].append(colunas[1].text)
            vendas['Id_Produto'].append(colunas[2].text)
            vendas['Data_venda'].append(colunas[3].text)
            vendas['Quantidade'].append(colunas[4].text)
            vendas['Valor_total'].append(colunas[5].text)
            vendas['Pedidos_concluido'].append(colunas[6].text)
            vendas['Avaliacao_servico'].append(colunas[7].text)
    break

executador.quit()

# Exportar planilha
df_vendas = pd.DataFrame(vendas)
df_vendas.to_excel("C:/Users/49439967870/Desktop/Ciência_de_dados/Hackaton_17_05/raspagem/tabelas/vendas.xlsx", index=False)

print(f"Arquivo 'vendas.xlsx' salvo com sucesso! {len(df_vendas)} linhas coletadas!")


