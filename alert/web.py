# web.py

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import date
from alert.gmail import enviar_email
from alert.sheets import autenticar, adicionar_valores_na_pagina, criar_nova_pagina, criar_nome_pagina
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import os.path
from webdriver_manager.chrome import ChromeDriverManager

def inicializar_navegador(url):
    MAX_RETRIES = 3
    for i in range(MAX_RETRIES):
        try:
            # Configurar as opções do navegador para o modo headless
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            
            # Inicializar o navegador com as opções configuradas
            browser = webdriver.Firefox(options=options)
            browser.get(url)
            sleep(1.0)
            return browser
        except Exception as e:
            print(f"Erro ao inicializar o navegador. Tentativa {i+1}/{MAX_RETRIES}")
            print(e)
            if i == MAX_RETRIES - 1:
                print("Número máximo de tentativas alcançado. Encerrando o programa.")
                exit(1)
            else:
                print("Esperando 10 segundos antes de tentar novamente...")
                sleep(10)
                
                
def fechar_navegador(browser):
    browser.quit()

def obter_dados_do_navegador():
    url = 'http://sjc.salvar.cemaden.gov.br/resources/graficos/interativo/grafico_CEMADEN.php?idpcd=7905&uf=MT'
    browser = inicializar_navegador(url)

    sleep(1)
    limpar_campo_cidade(browser)
    
    wait = WebDriverWait(browser, 1)
    tabela = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
    dados = extrair_dados(tabela)

    sleep(1)
    fechar_navegador(browser)
    return dados

def extrair_dados(tabela):
    soup = BeautifulSoup(tabela.get_attribute('outerHTML'), 'html.parser')
    linhas = soup.find_all('tr')
    dados = []

    for linha in linhas:
        colunas = linha.find_all('td')
        if len(colunas) > 8:
            cidade = colunas[1].text.strip()
            local = colunas[2].text.strip()
            precipitacao = colunas[8].text.strip()
            dados.append([cidade, local, precipitacao])

    return dados

def limpar_campo_cidade(browser):
    campo_cidade = browser.find_element(By.ID, "tboxCidade")
    campo_cidade.clear()

def verificar_enviar_email(dados):
    valor_limite = 5.0
    dados_com_excesso = []

    for cidade, local, precipitacao in dados:
        if precipitacao != '-' and float(precipitacao) > valor_limite:
            dados_com_excesso.append((cidade, local, precipitacao))

    if dados_com_excesso:
        enviar_email(dados_com_excesso)

def main():
    try:
        nome_pagina = criar_nome_pagina()
        criar_nova_pagina(nome_pagina)
        creds = autenticar()
        if creds is None:
            print("Não foi possível autenticar. Encerrando o programa.")
            exit(1)
        dados_do_navegador = obter_dados_do_navegador()
        if not dados_do_navegador:
            print("Não foi possível obter dados do navegador. Encerrando o programa.")
            exit(1)
        adicionar_valores_na_pagina(creds, nome_pagina, dados_do_navegador)
        verificar_enviar_email(dados_do_navegador)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == '__main__':
    main()

