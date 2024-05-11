import os
import ntpath
import sys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import pandas as pd

def init_webdriver(default=True, headless=False, output:str=None):
    """Inicia navegador automatizado google chrome

    Args:
        default (bool, optional): Define se navegador será aberto com opções padrão. Defaults to True.
        headless (bool, optional): Define se navegador abrirá com interface. Defaults to False.
        saida (str, optional): Diretório para downloads. Defaults to None.

    Returns:
        webdriver: navegador automatizado google chrome configurado
    """
    try:
        print('Iniciando navegador automatizado google chrome')
        s=Service(ChromeDriverManager().install())
        if default:
            if headless:
                driver = webdriver.Chrome(service=s, options=optionsChrome(headless=True, download_output=output))
            else:    
                driver = webdriver.Chrome(service=s, options=optionsChrome(headless=False, download_output=output))    
        else:
            # caminho das extensões
            extension_path = os.path.join(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0], 'extensions')
            extensions = [os.path.join(extension_path, 'popup_blocker.crx'), os.path.join(extension_path, 'enable_right_click.crx')]
            # extension = [os.path.join(extension_path, 'adblock.crx'), os.path.join(extension_path, 'enable_right_click.crx')]
            # extension = [os.path.join(extension_path, 'enable_right_click.crx')]
            try:
                if headless:
                    driver = webdriver.Chrome(service=s, options=optionsChrome(headless=True, download_output=output, crx_extension=extensions))
                else:
                    driver = webdriver.Chrome(service=s, options=optionsChrome(headless=False, download_output=output, crx_extension=extensions))
            except:
                if headless:
                    driver = webdriver.Chrome(service=s, options=optionsChrome(headless=True, download_output=output))
                else:
                    driver = webdriver.Chrome(service=s, options=optionsChrome(headless=False, download_output=output))
        return driver
    except:
        exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(init_webdriver.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
        sys.exit()

def optionsChrome(headless=False, download_output=None, crx_extension:list=None):
    """Configura opções do navegador chrome

    Args:
        headless (bool, optional): Define se navegador irá iniciar sem interface. Defaults to False.
        download_output (str, optional): Define diretorio para downloads. Defaults to None.
        crx_extension (list, optional): Listas de extensões para instalar no navegador. Defaults to None.

    Returns:
        Options: objeto contendo todas as opções configuradas do navegador
    """
    # Criar uma instância dr opções Chrome e devolvê-lo. Esta é a primeira chamada que você quer executar
    try:
        chrome_options = Options()
        if(headless):
            chrome_options.add_argument("--headless")
        prefs = {}
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0")
        binary_location = verify_chrome()
        chrome_options.binary_location = binary_location
        if download_output:
            download_output = os.path.normpath(download_output)
            download_output = download_output.replace('/',ntpath.sep)
            prefs.update({"download.default_directory" : download_output})
        if crx_extension:
            for extension in crx_extension:
                chrome_options.add_extension(extension)
        chrome_options.add_experimental_option('prefs', prefs)
        return chrome_options
        
    except:
        exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('ERRO DURANTE EXECUÇÃO {}: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(optionsChrome.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))
        
def verify_chrome():
    """Verifica se existe navegador chrome instalado e retorna o binario do navegador

    Returns:
        str: caminho do binário do navegador chrome
    """
    # Retorna o caminho para o executável mais recente do Chrome x32 ou X86. Isso é baseado na presença de um arquivo
    results_32 = [x for x in os.listdir(os.environ['PROGRAMFILES']) if re.search(r'(google)', x, re.IGNORECASE)]
    results_64 = [x for x in os.listdir(os.environ['PROGRAMFILES(X86)']) if re.search(r'(google)', x, re.IGNORECASE)]
    # Retorna o navegador da base de dados.
    if results_32:
        chrome_path = os.path.join(os.environ['PROGRAMFILES'], results_32[0], 'Chrome', 'Application')
        files = [x for x in os.listdir(chrome_path) if re.search(r'.exe$', x)]
        # Retorna o primeiro arquivo na lista de arquivos.
        if len(files) == 1:
            file = files[0]
        else:
            file = [x for x in files if re.search(r'chrome.exe', x)][0]
        
        browser_path = os.path.join(chrome_path,file)
        return browser_path
    elif results_64:
        chrome_path = os.path.join(os.environ['PROGRAMFILES(X86)'], results_64[0], 'Chrome', 'Application')
        files = [x for x in os.listdir(chrome_path) if re.search(r'.exe$', x)]
        # Retorna o primeiro arquivo na lista de arquivos.
        if len(files) == 1:
            file = files[0]
        else:
            file = [x for x in files if re.search(r'chrome.exe', x)][0]
        browser_path = os.path.join(chrome_path, file)
        return browser_path
    else:
        print("Navegador não instalado")
        return None
        
def web_scrap(url:str=None, markup:str=None):
    """Realiza requisição em site e/ou obtem o conteudo do HTML

    Args:
        url (str, optional): URL a ser requisitada. Defaults to None.
        markup (str, optional): conteudo HTML. Defaults to None.

    Returns:
        bs4.BeautifulSoup: objeto BeautifulSoup
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    soup = None
    feature = 'html.parser'
    # cria instancia do BeautifulSoup com html informado
    if markup:
        soup = BeautifulSoup(markup, feature)
    # cria instancia do BeautifulSoup com html obtido pela requisição
    elif url:
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.content, feature)
    return soup

def scrap_terabyte(driver):
    zero_results = driver.find_elements(By.XPATH, '//h1[@class="busca-zerada"]') 
    elements = driver.find_elements(By.XPATH, '//div[contains(@class, "pbox")]')
    dict_products = {'Loja': 'Terabyte', 'Nome produto': [], 'Preço a vista': [], 'Preço parcelado': [], 'Link produto': []}

    for element in elements:
        if element.find_elements(By.CLASS_NAME, 'tbt_esgotado'): 
            continue
        link = element.find_element(By.TAG_NAME, 'a')
        link_product = link.get_attribute('href')
        data_link = web_scrap(url=link_product)
        pay_in_cash = data_link.find(id='valVista').text if data_link.find(id='valVista') else ''
        pay_by_installments = data_link.find_all('span', class_='valParc')[-1].text if data_link.find(id='valVista') else ''
        title_product = data_link.find('h1', class_='tit-prod').text if data_link.find('h1', class_='tit-prod') else ''
        dict_products.get('Nome produto').append(title_product)
        dict_products.get('Preço a vista').append(pay_in_cash)
        dict_products.get('Preço parcelado').append(pay_by_installments)
        dict_products.get('Link produto').append(link_product)
        print(title_product, pay_in_cash, pay_by_installments, link_product)
        sleep(2)
    df_products = pd.DataFrame.from_dict(dict_products)
    df_products.to_excel("output.xlsx")  



def scrap_kabum(): ...

def scrap_pichau(): ...

def scrap_amazon(): ...

def scrap_mercadolivre(): ...

item = input('Digite o item que deseja buscar-> ')

driver = init_webdriver()

urls = [
    f"https://www.terabyteshop.com.br/busca?str={item}",
    f"https://www.kabum.com.br/busca/{item}",
    f"https://www.pichau.com.br/search?q={item}",
    f"https://www.amazon.com.br/s?k={item}",
    f"https://lista.mercadolivre.com.br/{item}"
    ]

for link in urls:
    driver.get(link)
    if 'terabyteshop' in link: 
        print(f"Busca por: {item} na Terabyte")
        scrap_terabyte(driver)
    elif 'kabum' in link:
        print(f"Busca por: {item} na Kabum")
        scrap_kabum()
    elif 'pichau' in link:
        print(f"Busca por: {item} na Pichau")
        scrap_pichau()
    elif 'amazon' in link:
        print(f"Busca por: {item} na Amazon")
        scrap_amazon()
    elif 'mercadolivre' in link:
        print(f"Busca por: {item} no Mercado Livre")
        scrap_mercadolivre()
    sleep(3)

driver.quit()