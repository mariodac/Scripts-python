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
from datetime import date

today = date.today()
today = today.strftime("%d-%m-%Y")

out_dir = os.path.join(os.environ['USERPROFILE'], 'Documents')

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/58.0.3029.110 Safari/537.36'
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

def scrap_terabyte(driver, item):
    try:
        zero_results = driver.find_elements(By.XPATH, '//h1[@class="busca-zerada"]') 
        if zero_results:
            print('Nenhum resultado encontrado')
            return
        dict_products = {'Nome produto': [], 'Preço a vista': [], 'Preço parcelado': [], 'Link produto': []}
        data_html = web_scrap(markup=driver.page_source)
        # elements = driver.find_elements(By.XPATH, '//div[contains(@class, "pbox")]')
        elements = data_html.find_all('div', class_='pbox')
        for element in elements:
            if element.find(class_='tbt_esgotado'): 
                continue
            # link = element.find_elements(By.TAG_NAME, 'a')[0] if element.find_elements(By.TAG_NAME, 'a') else None
            link = element.find('a') if element.find('a') else None
            # link_product = link.get_attribute('href')
            link_product = link.get('href')
            r'(\d+(\.)?)+(\,\d{1,2})?'
            # all_text = element.find_elements(By.CLASS_NAME, 'prod-new-price')[0].text if element.find_elements(By.CLASS_NAME, 'prod-new-price') else ''
            all_text = element.find('div', class_='prod-new-price').text if element.find('div', class_='prod-new-price') else ''
            pay_in_cash = re.search(r'(\d+(\.)?)+(\,\d{1,2})?', all_text).group() if re.search(r'(\d+(\.)?)+(\,\d{1,2})?', all_text) else ''
            # all_text = element.find_elements(By.CLASS_NAME, 'prod-juros')[0].text if element.find_elements(By.CLASS_NAME, 'prod-juros') else ''
            all_text = element.find(class_='prod-juros').text if element.find(class_='prod-juros') else ''
            texts = re.findall(r'(\d+)+(\,\d{1,2})?', all_text)
            if not texts:
                pay_by_installments = ''
            else:
                parcels = int(''.join(texts[0]))
                value_parcel = float(''.join(texts[1]).replace(',', '.'))
                pay_by_installments = round(parcels * value_parcel, 2)
            # title_product = element.find_elements(By.CLASS_NAME, 'prod-name')[0].text if element.find_elements(By.CLASS_NAME, 'prod-name') else ''
            title_product = element.find(class_='prod-name').text if element.find(class_='prod-name') else ''
            dict_products.get('Nome produto').append(title_product)
            dict_products.get('Preço a vista').append(pay_in_cash)
            dict_products.get('Preço parcelado').append(pay_by_installments)
            dict_products.get('Link produto').append(link_product)
            # print(title_product, pay_in_cash, pay_by_installments, link_product)
            sleep(2)
        df_products = pd.DataFrame.from_dict(dict_products)
        out_file = os.path.join(out_dir, f"terabyte_{today}_{item.replace(' ', '_')}.xlsx")
        df_products.to_excel(out_file)
    except:
        exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('ERRO DURANTE EXECUÇÃO scrap_terabyte: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))

def scrap_kabum(driver:webdriver.Chrome, item:str): 
    try:
        zero_results = driver.find_elements(By.ID, 'listingEmpty')
        if zero_results:
            print('Nenhum resultado encontrado')
            return
        dict_products = {'Nome produto': [], 'Preço a vista': [], 'Preço parcelado': [], 'Link produto': []}
        # elements = driver.find_elements(By.XPATH, '//article[contains(@class, "productCard")]')
        data_html = web_scrap(markup=driver.page_source)
        for element in data_html.find_all('article', class_='productCard'):
            link_product = 'https://www.kabum.com.br' + element.a.get('href') if element.a else ''
            data_link = web_scrap(url=link_product)
            pay_by_installments = data_link.find('b', class_='regularPrice').text if data_link.find('b', class_='regularPrice') else ''
            pay_in_cash = data_link.find('h4', class_='finalPrice').text if data_link('h4', class_='finalPrice') else ''
            title_product = data_link.find('h1').text if data_link.find('h1') else ''
            dict_products.get('Nome produto').append(title_product)
            dict_products.get('Preço a vista').append(pay_in_cash)
            dict_products.get('Preço parcelado').append(pay_by_installments)
            dict_products.get('Link produto').append(link_product)
        df_products = pd.DataFrame.from_dict(dict_products)
        out_file = os.path.join(out_dir, f"kabum_{today}_{item.replace(' ', '_')}.xlsx")
        df_products.to_excel(out_file)
    except:
        exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('ERRO DURANTE EXECUÇÃO scrap_kabum: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))

def scrap_pichau(driver:webdriver.Chrome, item:str): 
    try:
        data_html = web_scrap(markup=driver.page_source)
        zero_results = data_html.find('p', class_='MuiTypography-root MuiTypography-h6')
        if zero_results:
            print('Nenhum resultado encontrado')
            return
        dict_products = {'Nome produto': [], 'Preço a vista': [], 'Preço parcelado': [], 'Link produto': []}
        elements = data_html.find_all('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-md-4 MuiGrid-grid-lg-3 MuiGrid-grid-xl-2')
        for element in elements:
            title_product = element.find('h2').text if  element.find('h2').text else ''
            link_product = 'https://www.pichau.com.br' + element.a.get('href') if element.a else ''
            # pay_in_cash = element.find('div', class_='jss230').text if element.find('div', class_='jss230') else ''
            # pay_by_installments = element.find('div', class_='jss257').text if element.find('div', class_='jss257') else ''
            pay_in_cash, pay_by_installments = [re.search(r'(^R\\$ )?(\d+(\.)?)+(\,\d{1,2})?', x.text, flags=re.UNICODE).group() for x in element.find_all('div') if re.search(r'(^R\\$ )?(\d+(\.)?)+(\,\d{1,2})?$', x.text, flags=re.UNICODE)]
            dict_products.get('Nome produto').append(title_product)
            dict_products.get('Preço a vista').append(pay_in_cash)
            dict_products.get('Preço parcelado').append(pay_by_installments)
            dict_products.get('Link produto').append(link_product)
        df_products = pd.DataFrame.from_dict(dict_products)
        out_file = os.path.join(out_dir, f"pichau_{today}_{item.replace(' ', '_')}.xlsx")
        df_products.to_excel(out_file)
    except:
        exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('ERRO DURANTE EXECUÇÃO scrap_pichau: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))

def scrap_amazon(driver:webdriver.Chrome, item:str): 
    try:
        input('Pressione qualquer tecla para continuar ...')
        data_html = web_scrap(markup=driver.page_source)
        zero_results = data_html.find('div', id='h')
        if zero_results:
            print('Nenhum resultado encontrado')
            return
        dict_products = {'Nome produto': [], 'Preço a vista': [], 'Preço parcelado': [], 'Link produto': []}
        elements = data_html.find_all('div', class_='sg-col-inner')
        for element in elements[5:]:
            pay_by_installments = element.find_all('span', class_='a-offscreen')[0].text if element.find_all('span', class_='a-offscreen') else ''
            pay_in_cash = element.find_all('span', class_='a-offscreen')[0].text if element.find_all('span', class_='a-offscreen') else ''
            title_product = element.find('span', class_='a-size-base-plus a-color-base a-text-normal').text if element.find('span', class_='a-size-base-plus a-color-base a-text-normal') else ''
            link_product = 'https://www.amazon.com.br' + element.a.get('href') if element.a else ''

            dict_products.get('Nome produto').append(title_product)
            dict_products.get('Preço a vista').append(pay_in_cash)
            dict_products.get('Preço parcelado').append(pay_by_installments)
            dict_products.get('Link produto').append(link_product)
        df_products = pd.DataFrame.from_dict(dict_products)
        out_file = os.path.join(out_dir, f"amazon_{today}_{item.replace(' ', '_')}.xlsx")
        df_products.to_excel(out_file)
    except:
        exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('ERRO DURANTE EXECUÇÃO scrap_amazon: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))

def scrap_mercadolivre(driver:webdriver.Chrome, item:str):
    try:
        data_html = web_scrap(markup=driver.page_source)
        dict_products = {'Nome produto': [], 'Preço a vista': [], 'Preço parcelado': [], 'Link produto': []}
        elements = data_html.find_all('li', class_='ui-search-layout__item')
        for element in elements:
            title_product = element.h2.text if element.h2 else ''
            pay_in_cash = element.find('span', class_='andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript').text if element.find('span', class_='andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript') else ''
            pay_by_installments = element.find('span', class_='andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript').text if element.find('span', class_='andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript') else ''
            link_product = element.a.get('href') if element.h2 else ''
            dict_products.get('Nome produto').append(title_product)
            dict_products.get('Preço a vista').append(pay_in_cash)
            dict_products.get('Preço parcelado').append(pay_by_installments)
            dict_products.get('Link produto').append(link_product)
        df_products = pd.DataFrame.from_dict(dict_products)
        out_file = os.path.join(out_dir, f"mercadolivre_{today}_{item.replace(' ', '_')}.xlsx")
        df_products.to_excel(out_file)
    except:
        exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('ERRO DURANTE EXECUÇÃO scrap_mercadolivre: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))

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
        scrap_terabyte(driver, item)
    if 'kabum' in link:
        print(f"Busca por: {item} na Kabum")
        scrap_kabum(driver, item)
    if 'pichau' in link:
        print(f"Busca por: {item} na Pichau")
        scrap_pichau(driver, item)
    if 'amazon' in link:
        print(f"Busca por: {item} na Amazon")
        scrap_amazon(driver, item)
    if 'mercadolivre' in link:
        print(f"Busca por: {item} no Mercado Livre")
        scrap_mercadolivre(driver, item)
    sleep(3)

driver.quit()